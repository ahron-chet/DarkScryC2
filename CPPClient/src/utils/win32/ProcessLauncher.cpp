#include "ProcessLauncher.hpp"
#include "Process.hpp"
#include "Security.hpp"
#include "UserUtils.hpp"
#include <sddl.h>

using namespace win32;
using namespace win32::security;
using namespace win32::process;

namespace {

bool duplicate_token_from_sid(const std::wstring& sid,
                              LaunchOptions& opt)
{
    DWORD pid{};
    if (!find_by_sid(sid, pid)) return false;

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

bool create_with_credentials(const CredentialsParam& cred,
                             LaunchOptions&          opt)
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

    switch (opt.method)
    {
    case CreationMethod::CurrentToken:
        return ::CreateProcessW(opt.executable.c_str(), nullptr, nullptr, nullptr,
                                TRUE, opt.flags, nullptr, nullptr, &opt.si, &opt.pi);

    case CreationMethod::ImpersonateDuplicateToken: {
        const auto& p = std::get<ImpersonateDuplicateTokenParam>(opt.params);
        if (!enable_privilege(L"SeDebugPrivilege")) return false;
        return duplicate_token_from_sid(p.sid, opt);
    }

    case CreationMethod::Credentials: {
        const auto& p = std::get<CredentialsParam>(opt.params);
        return create_with_credentials(p, opt);
    }
    }
    return false;
}
