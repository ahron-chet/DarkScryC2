#pragma once
#include <Windows.h>
#include <functional>
#include <string>
#include <TlHelp32.h>

namespace win32::process {

void for_each(const std::function<bool(const PROCESSENTRY32W&)>& cb);
bool find_by_sid(const std::wstring& sid, DWORD& pid);

} // namespace win32::process
