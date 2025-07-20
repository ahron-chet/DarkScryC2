#pragma once

#include <string>

namespace win32::user {

	// Gets the SID of the current process user.
	std::wstring get_current_user_sid();

	// Gets the user name of the current process user.
	std::wstring get_current_user_name();

	// Retrieves SID by user name. Returns empty string if user doesn't exist or on failure.
	std::wstring get_sid_by_user_name(const std::wstring& name);

	// Retrieves user name by SID. Returns empty string if SID doesn't exist or on failure.
	std::wstring get_name_by_sid(const std::wstring& sid);

} // namespace win32::user
