#pragma once
#include <Windows.h>
#include <string>
#include "WinHandle.hpp"

namespace win32::security {

bool enable_privilege(const wchar_t* name);
std::wstring sid_to_string(PSID sid);
bool process_matches_sid(DWORD pid, const std::wstring& sid);

} // namespace win32::security
