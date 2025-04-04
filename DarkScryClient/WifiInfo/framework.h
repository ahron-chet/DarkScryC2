#pragma once

#define WIN32_LEAN_AND_MEAN             // Exclude rarely-used stuff from Windows headers
// Windows Header Files
#include <windows.h>
#include <wlanapi.h>
#include <objbase.h>
#include <vector>
#include <string>
#include <cwchar>
#include <cstdio>


#pragma comment(lib, "wlanapi.lib")
#pragma comment(lib, "ole32.lib")