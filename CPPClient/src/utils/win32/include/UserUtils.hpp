#pragma once
#include <Windows.h>
#include <string>

namespace win32::user {

// Returns the SID string for a given user name. Empty string on failure.
std::wstring get_sid_by_user_name(const std::wstring& name);

} // namespace win32::user
