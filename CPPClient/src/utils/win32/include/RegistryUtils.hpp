#pragma once
#include <Windows.h>
#include <string>

namespace win32::registry {

std::wstring reg_query_string(HKEY root,
                              const wchar_t* sub_key,
                              const wchar_t* value,
                              const wchar_t* fallback);

std::string narrow(const std::wstring& ws);

} // namespace win32::registry
