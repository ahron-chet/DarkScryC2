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

std::string registry::narrow(const std::wstring& ws)
{
    if (ws.empty()) return {};
    int len = WideCharToMultiByte(CP_UTF8, 0, ws.data(), (int)ws.size(),
                                  nullptr, 0, nullptr, nullptr);
    std::string s(len, '\0');
    WideCharToMultiByte(CP_UTF8, 0, ws.data(), (int)ws.size(),
                        s.data(), len, nullptr, nullptr);
    return s;
}
