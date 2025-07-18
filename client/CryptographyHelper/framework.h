#pragma once

#define WIN32_LEAN_AND_MEAN             // Exclude rarely-used stuff from Windows headers
// Windows Header Files
#include <windows.h>
#include <wincrypt.h>
#include <iostream>
#include <vector>
#include <string>

#pragma comment(lib, "Crypt32.lib")

std::vector<BYTE> Base64Decode(const std::string& base64String);
std::string Base64Encode(const std::vector<BYTE>& data);