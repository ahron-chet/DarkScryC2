#pragma once
#include <Windows.h>
#include <string>

namespace win32::registry {

std::wstring reg_query_string(HKEY root,
                              const wchar_t* sub_key,
                              const wchar_t* value,
                              const wchar_t* fallback);

DWORD reg_query_dword(HKEY root,
                      const wchar_t* sub_key,
                      const wchar_t* value,
                      DWORD fallback);

bool reg_set_string(HKEY root,
                    const wchar_t* sub_key,
                    const wchar_t* value,
                    const std::wstring& data);

bool reg_set_dword(HKEY root,
                   const wchar_t* sub_key,
                   const wchar_t* value,
                   DWORD data);

} // namespace win32::registry
