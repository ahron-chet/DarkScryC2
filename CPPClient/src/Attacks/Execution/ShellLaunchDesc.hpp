#pragma once
#include <string>
#include <optional>

/// One neutral description that *any* platform can understand.
enum class ShellLaunchKind {
    CurrentUser,          // run under caller’s token
    ImpersonateSid,       // duplicate an existing logon session
    Credentials           // explicit username / password
};

struct ShellLaunchDesc
{
    ShellLaunchKind            kind { ShellLaunchKind::CurrentUser };

    // ─── only when kind == ImpersonateSid ──────────────────
    std::wstring               sid;

    // ─── only when kind == Credentials ───────────────────
    std::optional<std::wstring> username;   // UPN or local (“DOMAIN\User”)
    std::optional<std::wstring> password;   // plaintext – lab use only
};
