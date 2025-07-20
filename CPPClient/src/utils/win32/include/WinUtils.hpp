#pragma once
#include <string>
#include <Windows.h>

namespace win32 {

std::string narrow(const std::wstring& ws);
std::wstring charToWchar(const char* utf8str);

} // namespace win32

