#pragma once
//
//  Generic process-launch helper for lab use only.
//  ───────────────────────────────────────────────
//  * Launch under current token            →  default
//  * Launch under an *existing* SID token →  set .sid
//  * Launch with explicit credentials      →  set .username + .password
//
//  NOTE: No attempt is made to protect credentials; this is for
//        contained simulation networks only.
//

#include <Windows.h>
#include <variant>
#include <optional>
#include <string>

#include "WinHandle.hpp"

namespace win32::process {

enum class CreationType {
    CurrentToken,
    TokenImpersonation,
    Credentials
};

struct TokenImpersonationParam {
    std::wstring sid;
};

struct CredentialsParam {
    std::optional<std::wstring> username;
    std::optional<std::wstring> password;
};

using LaunchParams = std::variant<std::monostate,
                                  TokenImpersonationParam,
                                  CredentialsParam>;

struct LaunchOptions
{
    std::wstring executable { L"C:\\Windows\\System32\\cmd.exe" };
    CreationType creation   { CreationType::CurrentToken };
    LaunchParams params;             // must match `creation`
    DWORD        flags      { CREATE_NO_WINDOW };
    STARTUPINFOW        si{};      // caller fills before launch
    PROCESS_INFORMATION pi{};      // filled on success

    static LaunchOptions current_token(std::wstring exe = {});
    static LaunchOptions impersonate_sid(std::wstring sid,
                                         std::wstring exe = {});
    static LaunchOptions credentials(std::wstring user,
                                     std::wstring pwd,
                                     std::wstring exe = {});
};

/// Launch a process as requested; returns true on success.
/// `opt.si` must be fully initialised by the caller (e.g. pipes).
bool launch(LaunchOptions& opt);

} // namespace win32::process
