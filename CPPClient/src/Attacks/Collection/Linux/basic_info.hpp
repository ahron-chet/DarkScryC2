#pragma once
#include <string>
#include <vector>

namespace linux_os::sysinfo {

    struct BasicMachineInfo {
        std::string host_name;
        std::string primary_ip;

        std::string operating_system;
        std::string os_version_detail;

        std::string cpu;
        std::string ram;
        std::string disk;
        std::string gpu;

        std::vector<std::string> logged_on_sessions;
    };

    [[nodiscard]]
    BasicMachineInfo get_basic_machine_info();

} // namespace linux_os::sysinfo
