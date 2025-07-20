#include "RegistryUtils.hpp"

using namespace win32;

std::wstring registry::reg_query_string(HKEY root,
                                        const wchar_t* sub_key,
                                        const wchar_t* value,
                                        const wchar_t* fallback)
{
    DWORD type = 0, bytes = 0;
    if (RegGetValueW(root, sub_key, value, RRF_RT_REG_SZ, &type, nullptr, &bytes) != ERROR_SUCCESS)
        return std::wstring{ fallback };

    std::wstring buffer(bytes / sizeof(wchar_t), L'\0');
    if (RegGetValueW(root, sub_key, value, RRF_RT_REG_SZ, nullptr, buffer.data(), &bytes) != ERROR_SUCCESS)
        return std::wstring{ fallback };
    buffer.resize((bytes / sizeof(wchar_t)) - 1); // drop trailing NULL
    return buffer;
}

DWORD registry::reg_query_dword(HKEY root,
                                const wchar_t* sub_key,
                                const wchar_t* value,
                                DWORD fallback)
{
    DWORD data = 0;
    DWORD bytes = sizeof(data);
    if (RegGetValueW(root, sub_key, value, RRF_RT_REG_DWORD, nullptr, &data, &bytes) != ERROR_SUCCESS)
        return fallback;
    return data;
}

bool registry::reg_set_string(HKEY root,
                              const wchar_t* sub_key,
                              const wchar_t* value,
                              const std::wstring& data)
{
    HKEY key = nullptr;
    if (RegCreateKeyExW(root, sub_key, 0, nullptr, 0, KEY_SET_VALUE, nullptr, &key, nullptr) != ERROR_SUCCESS)
        return false;
    bool ok = RegSetValueExW(key, value, 0, REG_SZ,
                             reinterpret_cast<const BYTE*>(data.c_str()),
                             static_cast<DWORD>((data.size() + 1) * sizeof(wchar_t))) == ERROR_SUCCESS;
    RegCloseKey(key);
    return ok;
}

bool registry::reg_set_dword(HKEY root,
                             const wchar_t* sub_key,
                             const wchar_t* value,
                             DWORD data)
{
    HKEY key = nullptr;
    if (RegCreateKeyExW(root, sub_key, 0, nullptr, 0, KEY_SET_VALUE, nullptr, &key, nullptr) != ERROR_SUCCESS)
        return false;
    bool ok = RegSetValueExW(key, value, 0, REG_DWORD,
                             reinterpret_cast<const BYTE*>(&data),
                             sizeof(DWORD)) == ERROR_SUCCESS;
    RegCloseKey(key);
    return ok;
}
