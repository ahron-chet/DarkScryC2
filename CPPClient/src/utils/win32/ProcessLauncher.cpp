#include "ProcessLauncher.hpp"
#include "Process.hpp"
#include "Security.hpp"
#include "UserUtils.hpp"
#include <sddl.h>

using namespace win32;
using namespace win32::security;
using namespace win32::process;

namespace {

bool create_with_sid(const std::wstring& sid,
                     LaunchOptions&       opt)
{
    std::wstring current = user::get_current_user_sid();

    // Same SID → spawn normally under current token
    if (_wcsicmp(sid.c_str(), current.c_str()) == 0)
        return ::CreateProcessW(opt.executable.c_str(), nullptr, nullptr, nullptr,
                                TRUE, opt.flags, nullptr, nullptr, &opt.si, &opt.pi);

    // Need SeDebugPrivilege to duplicate another users’ token
    if (!enable_privilege(L"SeDebugPrivilege"))
        return false;

    DWORD pid{};
    if (!find_by_sid(sid, pid))
        return false;

    unique_handle hProc(::OpenProcess(PROCESS_QUERY_INFORMATION, FALSE, pid));
    if (!hProc) return false;

    HANDLE hTok{};
    if (!::OpenProcessToken(hProc.get(),
                            TOKEN_DUPLICATE | TOKEN_ASSIGN_PRIMARY | TOKEN_QUERY,
                            &hTok))
        return false;
    unique_handle tok(hTok);

    HANDLE hDup{};
    if (!::DuplicateTokenEx(tok.get(), MAXIMUM_ALLOWED, nullptr,
                            SecurityIdentification, TokenPrimary, &hDup))
        return false;
    unique_handle dup(hDup);

    return ::CreateProcessWithTokenW(dup.get(), 0,
                                     opt.executable.c_str(), nullptr,
                                     opt.flags,
                                     nullptr, nullptr, &opt.si, &opt.pi);
}

bool create_with_logon(const CredentialsParam& cred,
                       LaunchOptions&       opt)
{
    const wchar_t* user = cred.username ? cred.username->c_str() : nullptr;
    const wchar_t* pass = cred.password ? cred.password->c_str() : L"";
    return ::CreateProcessWithLogonW(user,        /*domain*/ nullptr,
                                     pass,        /*LOGON_WITH_PROFILE*/ 0,
                                     opt.executable.c_str(), nullptr,
                                     opt.flags,
                                     nullptr, nullptr, &opt.si, &opt.pi);
}

} // namespace

// ------------------------------------------------------------------
//  public façade
// ------------------------------------------------------------------
bool process::launch(LaunchOptions& opt)
{
    ZeroMemory(&opt.pi, sizeof(opt.pi));

    switch (opt.creation) {
    case CreationType::CurrentToken:
        return ::CreateProcessW(opt.executable.c_str(), nullptr, nullptr, nullptr,
                                TRUE, opt.flags, nullptr, nullptr, &opt.si, &opt.pi);

    case CreationType::TokenImpersonation: {
        const auto& p = std::get<TokenImpersonationParam>(opt.params);
        return create_with_sid(p.sid, opt);
    }

    case CreationType::Credentials: {
        const auto& p = std::get<CredentialsParam>(opt.params);
        return create_with_logon(p, opt);
    }
    }
    return false;
}

// ------------------------------------------------------------------
//  LaunchOptions factories
// ------------------------------------------------------------------
LaunchOptions LaunchOptions::current_token(std::wstring exe)
{
    LaunchOptions opt;
    if (!exe.empty()) opt.executable = std::move(exe);
    opt.creation = CreationType::CurrentToken;
    opt.params = std::monostate{};
    return opt;
}

LaunchOptions LaunchOptions::impersonate_sid(std::wstring sid,
                                             std::wstring exe)
{
    LaunchOptions opt;
    if (!exe.empty()) opt.executable = std::move(exe);
    opt.creation = CreationType::TokenImpersonation;
    opt.params = TokenImpersonationParam{ std::move(sid) };
    return opt;
}

LaunchOptions LaunchOptions::credentials(std::wstring user,
                                         std::wstring pwd,
                                         std::wstring exe)
{
    LaunchOptions opt;
    if (!exe.empty()) opt.executable = std::move(exe);
    opt.creation = CreationType::Credentials;
    opt.params = CredentialsParam{ std::move(user), std::move(pwd) };
    return opt;
}
