#include "WinUtils.hpp"
#include <Windows.h>
#include <string>

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

