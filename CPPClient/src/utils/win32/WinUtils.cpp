#include "WinUtils.hpp"
#include <Windows.h>
#include <string>
#include <codecvt>
#include <locale>

using namespace win32;

std::string win32::narrow(const std::wstring& ws)
{
    if (ws.empty()) return {};
    int len = ::WideCharToMultiByte(CP_UTF8, 0, ws.data(), static_cast<int>(ws.size()),
                                    nullptr, 0, nullptr, nullptr);
    std::string s(len, '\0');
    ::WideCharToMultiByte(CP_UTF8, 0, ws.data(), static_cast<int>(ws.size()),
                          s.data(), len, nullptr, nullptr);
    return s;
}

std::wstring win32::charToWchar(const char* utf8str)
{
    if (!utf8str) return L"";

    std::wstring_convert<std::codecvt_utf8_utf16<wchar_t>> converter;
    return converter.from_bytes(utf8str);
}

