#include "basic_info.hpp"

#include <unistd.h>
#include <sys/utsname.h>
#include <sys/statvfs.h>
#include <ifaddrs.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <net/if.h>
#include <utmpx.h>

#include <fstream>
#include <sstream>
#include <vector>

namespace {

std::string get_os_name() {
    std::ifstream f("/etc/os-release");
    std::string line;
    while (std::getline(f, line)) {
        if (line.rfind("PRETTY_NAME=", 0) == 0) {
            std::string val = line.substr(12);
            if (!val.empty() && val.front() == '"' && val.back() == '"')
                val = val.substr(1, val.size() - 2);
            return val;
        }
    }
    return "Linux";
}

std::string get_os_version() {
    struct utsname uts{};
    if (uname(&uts) == 0)
        return uts.release;
    return {};
}

std::string get_cpu_name() {
    std::ifstream f("/proc/cpuinfo");
    std::string line;
    while (std::getline(f, line)) {
        if (line.rfind("model name", 0) == 0) {
            auto pos = line.find(':');
            if (pos != std::string::npos) {
                std::string name = line.substr(pos + 1);
                while (!name.empty() && isspace(name.front())) name.erase(name.begin());
                return name;
            }
        }
    }
    return "Unknown CPU";
}

std::string bytes_to_gb(unsigned long long bytes, int precision = 0) {
    double gb = static_cast<double>(bytes) / (1024.0 * 1024.0 * 1024.0);
    std::ostringstream oss;
    oss.setf(std::ios::fixed, std::ios::floatfield);
    oss.precision(precision);
    oss << gb << " GB";
    return oss.str();
}

std::string get_total_ram() {
    std::ifstream f("/proc/meminfo");
    std::string line;
    while (std::getline(f, line)) {
        if (line.rfind("MemTotal:", 0) == 0) {
            std::istringstream iss(line.substr(9));
            unsigned long kb;
            iss >> kb;
            return bytes_to_gb(kb * 1024ULL, 1);
        }
    }
    return "Unknown RAM";
}

std::string get_disk_size() {
    struct statvfs sv{};
    if (statvfs("/", &sv) == 0) {
        unsigned long long bytes = static_cast<unsigned long long>(sv.f_frsize) * sv.f_blocks;
        return bytes_to_gb(bytes, 0);
    }
    return "Unknown Disk";
}

std::string get_primary_ipv4() {
    struct ifaddrs* ifaddr = nullptr;
    if (getifaddrs(&ifaddr) == -1)
        return "N/A";
    std::string ip = "N/A";
    for (auto* ifa = ifaddr; ifa; ifa = ifa->ifa_next) {
        if (!ifa->ifa_addr) continue;
        if (ifa->ifa_addr->sa_family == AF_INET && !(ifa->ifa_flags & IFF_LOOPBACK)) {
            char buf[INET_ADDRSTRLEN];
            auto* sa = reinterpret_cast<struct sockaddr_in*>(ifa->ifa_addr);
            if (inet_ntop(AF_INET, &sa->sin_addr, buf, sizeof(buf))) {
                ip = buf;
                break;
            }
        }
    }
    freeifaddrs(ifaddr);
    return ip;
}

std::vector<std::string> get_logged_on_users() {
    std::vector<std::string> users;
    setutxent();
    struct utmpx* ent;
    while ((ent = getutxent()) != nullptr) {
        if (ent->ut_type == USER_PROCESS)
            users.emplace_back(ent->ut_user);
    }
    endutxent();
    return users;
}

} // namespace

namespace linux_os::sysinfo {

BasicMachineInfo get_basic_machine_info() {
    BasicMachineInfo info;
    char host[256]{};
    if (gethostname(host, sizeof(host)) == 0)
        info.host_name = host;
    else
        info.host_name = "unknown";

    info.primary_ip = get_primary_ipv4();
    info.operating_system = get_os_name();
    info.os_version_detail = get_os_version();
    info.cpu = get_cpu_name();
    info.ram = get_total_ram();
    info.disk = get_disk_size();
    info.gpu = "N/A";
    info.logged_on_sessions = get_logged_on_users();
    return info;
}

} // namespace linux_os::sysinfo

