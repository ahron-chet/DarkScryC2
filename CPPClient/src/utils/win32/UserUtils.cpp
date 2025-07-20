#include "UserUtils.hpp"
#include "Security.hpp"
#include <Windows.h>
#include <vector>
#include <sddl.h>

namespace win32::user {

    std::wstring get_current_user_sid() {
        HANDLE token = nullptr;
        if (!::OpenProcessToken(::GetCurrentProcess(), TOKEN_QUERY, &token)) {
            return {};
        }

        DWORD size = 0;
        ::GetTokenInformation(token, TokenUser, nullptr, 0, &size);
        if (::GetLastError() != ERROR_INSUFFICIENT_BUFFER) {
            ::CloseHandle(token);
            return {};
        }

        std::vector<std::byte> buffer(size);
        if (!::GetTokenInformation(token, TokenUser, buffer.data(), size, &size)) {
            ::CloseHandle(token);
            return {};
        }

        PTOKEN_USER user = reinterpret_cast<PTOKEN_USER>(buffer.data());
        std::wstring sid = security::sid_to_string(user->User.Sid);

        ::CloseHandle(token);
        return sid;
    }

    std::wstring get_current_user_name() {
        wchar_t name[256];
        DWORD name_size = 256;

        if (!::GetUserNameW(name, &name_size)) {
            return {};
        }

        return { name, name_size - 1 }; // remove null-terminator
    }

    std::wstring get_sid_by_user_name(const std::wstring& name) {
        DWORD sid_size = 0, domain_size = 0;
        SID_NAME_USE use;

        ::LookupAccountNameW(nullptr, name.c_str(), nullptr, &sid_size,
            nullptr, &domain_size, &use);
        if (::GetLastError() != ERROR_INSUFFICIENT_BUFFER) {
            return {};
        }

        std::vector<std::byte> sid_buf(sid_size);
        std::vector<wchar_t> domain_buf(domain_size);

        if (!::LookupAccountNameW(nullptr, name.c_str(), sid_buf.data(), &sid_size,
            domain_buf.data(), &domain_size, &use)) {
            return {};
        }

        return security::sid_to_string(static_cast<PSID>(sid_buf.data()));
    }

    std::wstring get_name_by_sid(const std::wstring& sid) {
        PSID sid_ptr = nullptr;
        if (!::ConvertStringSidToSidW(sid.c_str(), &sid_ptr)) {
            return {};
        }

        DWORD name_size = 0, domain_size = 0;
        SID_NAME_USE use;

        ::LookupAccountSidW(nullptr, sid_ptr, nullptr, &name_size,
            nullptr, &domain_size, &use);
        if (::GetLastError() != ERROR_INSUFFICIENT_BUFFER) {
            ::LocalFree(sid_ptr);
            return {};
        }

        std::vector<wchar_t> name_buf(name_size);
        std::vector<wchar_t> domain_buf(domain_size);

        if (!::LookupAccountSidW(nullptr, sid_ptr, name_buf.data(), &name_size,
            domain_buf.data(), &domain_size, &use)) {
            ::LocalFree(sid_ptr);
            return {};
        }

        ::LocalFree(sid_ptr);
        return { name_buf.data(), name_size };
    }

} // namespace win32::user