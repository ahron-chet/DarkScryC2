#include "pch.h"


struct WifiProfile
{
    LPWSTR ssid;
    LPWSTR xml;
};

static LPWSTR AllocCoTaskMemString(const std::wstring& source)
{
    if (source.empty())
        return nullptr;

    const size_t bufSize = (source.size() + 1) * sizeof(wchar_t);
    LPWSTR result = static_cast<LPWSTR>(CoTaskMemAlloc(bufSize));
    if (result)
    {
        wcsncpy_s(result, source.size() + 1, source.c_str(), _TRUNCATE);
    }
    return result;
}


extern "C" __declspec(dllexport)
WifiProfile* GetWifiProfiles(int* count)
{
    if (!count) return nullptr;
    *count = 0;

    DWORD negotiatedVersion = 0;
    HANDLE hClient = nullptr;
    DWORD ret = WlanOpenHandle(2, nullptr, &negotiatedVersion, &hClient);
    if (ret != ERROR_SUCCESS)
    {
        return nullptr;
    }

    PWLAN_INTERFACE_INFO_LIST pIfList = nullptr;
    ret = WlanEnumInterfaces(hClient, nullptr, &pIfList);
    if (ret != ERROR_SUCCESS || !pIfList)
    {
        WlanCloseHandle(hClient, nullptr);
        return nullptr;
    }

    std::vector<WifiProfile> profiles;

    for (DWORD i = 0; i < pIfList->dwNumberOfItems; ++i)
    {
        GUID ifaceGuid = pIfList->InterfaceInfo[i].InterfaceGuid;

        PWLAN_PROFILE_INFO_LIST pProfileList = nullptr;
        ret = WlanGetProfileList(hClient, &ifaceGuid, nullptr, &pProfileList);
        if (ret == ERROR_SUCCESS && pProfileList)
        {
            for (DWORD j = 0; j < pProfileList->dwNumberOfItems; j++)
            {
                const WLAN_PROFILE_INFO& pi = pProfileList->ProfileInfo[j];
                LPWSTR xmlPtr = nullptr;
                DWORD flags = WLAN_PROFILE_GET_PLAINTEXT_KEY;
                DWORD grantedAccess = 0;

                DWORD gpRet = WlanGetProfile(
                    hClient,
                    &ifaceGuid,
                    pi.strProfileName,
                    nullptr,
                    &xmlPtr,
                    &flags,
                    &grantedAccess
                );
                if (gpRet == ERROR_SUCCESS && xmlPtr)
                {
                    std::wstring ssidStr(pi.strProfileName);
                    std::wstring xmlStr(xmlPtr);

                    WifiProfile wp{};
                    wp.ssid = AllocCoTaskMemString(ssidStr);
                    wp.xml = AllocCoTaskMemString(xmlStr);

                    profiles.push_back(wp);

                    WlanFreeMemory(xmlPtr);
                }
            }
            WlanFreeMemory(pProfileList);
        }
    }

    WlanFreeMemory(pIfList);
    WlanCloseHandle(hClient, nullptr);

    if (profiles.empty())
    {
        return nullptr;
    }

    *count = static_cast<int>(profiles.size());
    const size_t totalSize = sizeof(WifiProfile) * profiles.size();

    WifiProfile* arr = static_cast<WifiProfile*>(CoTaskMemAlloc(totalSize));
    if (!arr)
    {
        *count = 0;
        return nullptr;
    }

    memcpy(arr, profiles.data(), totalSize);

    return arr;
}
