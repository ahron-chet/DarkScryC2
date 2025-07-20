#pragma once
#ifdef _WIN32
#include "Windows/Shell.hpp"
namespace execution { using Shell = win32::Shell; }
#else
#include "Linux/Shell.hpp"
namespace execution { using Shell = linux_os::Shell; }
#endif
