#include "Security.hpp"
#include <sddl.h>
#include <vector>

using namespace win32;

bool security::enable_privilege(const wchar_t* name) {
    HANDLE hTok{};
    if (!::OpenProcessToken(::GetCurrentProcess(), TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY, &hTok))
        return false;
    win32::unique_handle tok(hTok);

    LUID luid{};
    if (!::LookupPrivilegeValueW(nullptr, name, &luid))
        return false;

    TOKEN_PRIVILEGES tp{};
    tp.PrivilegeCount           = 1;
    tp.Privileges[0].Luid       = luid;
    tp.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED;

    ::AdjustTokenPrivileges(tok.get(), FALSE, &tp, sizeof(tp), nullptr, nullptr);
    return ::GetLastError() == ERROR_SUCCESS;
}

std::wstring security::sid_to_string(PSID sid) {
    LPWSTR s = nullptr;
    if (::ConvertSidToStringSidW(sid, &s)) {
        std::wstring res{s};
        ::LocalFree(s);
        return res;
    }
    return {};
}

bool security::process_matches_sid(DWORD pid, const std::wstring& sid) {
    win32::unique_handle hProc(::OpenProcess(PROCESS_QUERY_INFORMATION, FALSE, pid));
    if (!hProc) return false;

    HANDLE hTok{};
    if (!::OpenProcessToken(hProc.get(), TOKEN_QUERY, &hTok))
        return false;
    win32::unique_handle tok(hTok);

    DWORD len{};
    ::GetTokenInformation(tok.get(), TokenUser, nullptr, 0, &len);
    if (::GetLastError() != ERROR_INSUFFICIENT_BUFFER) return false;

    std::vector<std::byte> buf(len);
    auto* p = reinterpret_cast<PTOKEN_USER>(buf.data());
    if (!::GetTokenInformation(tok.get(), TokenUser, p, len, &len))
        return false;

    return _wcsicmp(sid_to_string(p->User.Sid).c_str(), sid.c_str()) == 0;
}
