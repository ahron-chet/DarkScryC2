#pragma once
//
//  Minimal helper that hides CreateProcess* / token plumbing.
//

#include <Windows.h>
#include <variant>
#include <optional>
#include <string>

#include "WinHandle.hpp"

namespace win32::process {

enum class CreationMethod {
    CurrentToken,
    ImpersonateDuplicateToken,
    Credentials
};

struct ImpersonateDuplicateTokenParam { std::wstring sid; };

struct CredentialsParam {
    std::optional<std::wstring> username;
    std::optional<std::wstring> password;
};

using LaunchParam = std::variant<std::monostate,
                                 ImpersonateDuplicateTokenParam,
                                 CredentialsParam>;

struct LaunchOptions
{
    std::wstring   executable { L"C:\\Windows\\System32\\cmd.exe" };
    CreationMethod method     { CreationMethod::CurrentToken };
    LaunchParam    params;                 // must match .method
    DWORD          flags      { CREATE_NO_WINDOW };

    STARTUPINFOW        si{};              // caller initialises
    PROCESS_INFORMATION pi{};              // filled on success
};

/// Launch a process as requested; returns true on success.
/// `opt.si` must be fully initialised by the caller (e.g. pipes).
bool launch(LaunchOptions& opt);

} // namespace win32::process
