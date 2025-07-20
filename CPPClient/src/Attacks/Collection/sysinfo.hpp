#pragma once
#ifdef _WIN32
#include "Windows/basic_info.hpp"
namespace sysinfo = win32::sysinfo;
#else
#include "Linux/basic_info.hpp"
namespace sysinfo = linux_os::sysinfo;
#endif
