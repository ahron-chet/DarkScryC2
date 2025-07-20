#include "UserUtils.hpp"
#include "Security.hpp"
#include <vector>

using namespace win32;

std::wstring user::get_sid_by_user_name(const std::wstring& name) {
    DWORD sid_size = 0, domain_size = 0;
    SID_NAME_USE use;

    ::LookupAccountNameW(nullptr, name.c_str(), nullptr, &sid_size,
                         nullptr, &domain_size, &use);
    if (GetLastError() != ERROR_INSUFFICIENT_BUFFER)
        return {};

    std::vector<std::byte> sid_buf(sid_size);
    std::wstring domain(domain_size, L'\0');

    if (!::LookupAccountNameW(nullptr, name.c_str(), sid_buf.data(), &sid_size,
                              domain.data(), &domain_size, &use))
        return {};

    domain.resize(domain_size);
    return security::sid_to_string(static_cast<PSID>(sid_buf.data()));
}
