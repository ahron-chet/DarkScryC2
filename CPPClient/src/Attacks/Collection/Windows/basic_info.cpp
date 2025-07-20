


#define WIN32_LEAN_AND_MEAN
#define _WIN32_WINNT 0x0600

#include <winsock2.h>
#include <ws2tcpip.h>
#include <Windows.h>
#include <iphlpapi.h>
#include <WtsApi32.h> 
#include "basic_info.hpp"
#include "WinHandle.hpp"
#include "RegistryUtils.hpp"

#pragma comment(lib, "iphlpapi.lib")
#pragma comment(lib, "wtsapi32.lib")

#include <array>
#include <sstream>
#include <vector>
#include <algorithm>
#include "../../../utils/GeneralUtils.hpp"


namespace {
    using namespace win32::registry;


    // ------------------------------------------------------------------
    // Individual collectors
    // ------------------------------------------------------------------

    std::string get_os_product_name()
    {
        auto w = reg_query_string(HKEY_LOCAL_MACHINE,
            LR"(SOFTWARE\Microsoft\Windows NT\CurrentVersion)",
            L"ProductName",
            L"Unknown Windows");
        return narrow(w);
    }

    std::string get_os_version_detail()
    {
        std::wstring rel = reg_query_string(HKEY_LOCAL_MACHINE,
            LR"(SOFTWARE\Microsoft\Windows NT\CurrentVersion)",
            L"ReleaseId", L"?");
        std::wstring disp = reg_query_string(HKEY_LOCAL_MACHINE,
            LR"(SOFTWARE\Microsoft\Windows NT\CurrentVersion)",
            L"DisplayVersion", L"?");
        return "ReleaseId=" + narrow(rel) + ", DisplayVersion=" + narrow(disp);
    }

    std::string get_cpu_name()
    {
        auto w = reg_query_string(HKEY_LOCAL_MACHINE,
            LR"(HARDWARE\DESCRIPTION\System\CentralProcessor\0)",
            L"ProcessorNameString",
            L"Unknown CPU");
        std::string s = narrow(w);
        s.erase(std::remove_if(s.begin(), s.end(), ::isspace), s.end()); // trim
        return s;
    }

    std::string get_total_ram()
    {
        MEMORYSTATUSEX m{ sizeof(MEMORYSTATUSEX) };
        if (!GlobalMemoryStatusEx(&m)) return "Unknown RAM";
        return utils::bytes_to_gb(m.ullTotalPhys, 1);
    }

    std::string get_system_drive_size()
    {
        wchar_t sys_root[MAX_PATH] = {};
        GetWindowsDirectoryW(sys_root, MAX_PATH);      // e.g. "C:\Windows"
        sys_root[3] = L'\0';                           //  →  "C:\"

        ULARGE_INTEGER total{}; ULARGE_INTEGER free{};
        if (GetDiskFreeSpaceExW(sys_root, nullptr, &total, &free))
        {
            std::wstring fs;
            fs.resize(MAX_PATH);
            GetVolumeInformationW(sys_root, nullptr, 0, nullptr, nullptr, nullptr,
                fs.data(), (DWORD)fs.size());
            fs.resize(wcslen(fs.data()));
            return utils::bytes_to_gb(total.QuadPart, 0) + " " + narrow(fs);
        }
        return "Unknown Disk";
    }

    std::string get_gpus()
    {
        std::vector<std::wstring> names;
        DISPLAY_DEVICEW dd{ sizeof(dd) };
        for (DWORD id = 0; EnumDisplayDevicesW(nullptr, id, &dd, 0); ++id)
        {
            if (dd.StateFlags & DISPLAY_DEVICE_PRIMARY_DEVICE)
                names.emplace_back(dd.DeviceString);
            dd.cb = sizeof(dd);
        }
        std::string joined;
        for (auto& w : names)
        {
            if (!joined.empty()) joined += ", ";
            joined += narrow(w);
        }
        return joined.empty() ? "Unknown GPU" : joined;
    }

    std::string get_primary_ipv4()
    {
        ULONG buf_len = 15 * 1024;
        std::vector<std::byte> buf(buf_len);

        IP_ADAPTER_ADDRESSES* aa = reinterpret_cast<IP_ADAPTER_ADDRESSES*>(buf.data());
        if (GetAdaptersAddresses(AF_INET, GAA_FLAG_SKIP_ANYCAST
            | GAA_FLAG_SKIP_MULTICAST | GAA_FLAG_SKIP_DNS_SERVER,
            nullptr, aa, &buf_len) != NO_ERROR)
            return "N/A";

        for (auto* a = aa; a; a = a->Next)
        {
            if (a->OperStatus != IfOperStatusUp) continue;
            if (a->IfType == IF_TYPE_SOFTWARE_LOOPBACK) continue;

            for (auto* u = a->FirstUnicastAddress; u; u = u->Next)
            {
                SOCKADDR_IN* sa = reinterpret_cast<SOCKADDR_IN*>(u->Address.lpSockaddr);
                char ip[INET_ADDRSTRLEN];
                InetNtopA(AF_INET, &sa->sin_addr, ip, sizeof(ip));
                return ip;
            }
        }
        return "N/A";
    }

    std::vector<std::string> get_logged_on_sessions()
    {
        PWTS_SESSION_INFO_1W sessions = nullptr;
        DWORD count = 0;

        if (!WTSEnumerateSessionsExW(WTS_CURRENT_SERVER_HANDLE, nullptr, 1,
            &sessions, &count))
            return {};

        std::vector<std::string> users;
        for (DWORD i = 0; i < count; ++i)
        {
            if (sessions[i].State != WTSActive) continue;

            LPWSTR uname = nullptr;
            DWORD bytes = 0;
            if (WTSQuerySessionInformationW(WTS_CURRENT_SERVER_HANDLE,
                sessions[i].SessionId, WTSUserName, &uname, &bytes) && bytes > 1)
            {
                users.push_back(narrow(uname));
                WTSFreeMemory(uname);
            }
        }

        WTSFreeMemory(sessions);
        return users;
    }


} // namespace

// ----------------------------------------------------------------------
// public façade
// ----------------------------------------------------------------------
namespace win32::sysinfo {

    BasicMachineInfo get_basic_machine_info()
    {
        BasicMachineInfo info;
        info.host_name = narrow([] {
            wchar_t c[MAX_COMPUTERNAME_LENGTH + 1]{};
            DWORD len = std::size(c);
            GetComputerNameW(c, &len);
            return std::wstring{ c };
            }());
        info.primary_ip = get_primary_ipv4();
        info.operating_system = get_os_product_name();
        info.os_version_detail = get_os_version_detail();
        info.cpu = get_cpu_name();
        info.ram = get_total_ram();
        info.disk = get_system_drive_size();
        info.gpu = get_gpus();
        info.logged_on_sessions = get_logged_on_sessions();
        return info;
    }
}
