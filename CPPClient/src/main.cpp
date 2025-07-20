#define NOMINMAX
#include "Agent.h"

#ifdef _WIN32
#  include "win32/include/UserUtils.hpp"
#endif

int main() {

#ifdef _WIN32
    std::wstring sid = win32::user::get_sid_by_user_name(L"Administrator");

    if (!sid.empty()) {
        std::wcout << L"Administrator SID: " << sid << std::endl;
    } else {
        std::wcout << L"Failed to get SID for Administrator." << std::endl;
    }
#endif

    CppAgent::Agent agent;
    bool ok = agent.run();
    return ok ? 0 : 1;
}
