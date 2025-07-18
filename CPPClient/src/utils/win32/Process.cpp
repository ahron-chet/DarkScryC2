#include "Process.hpp"
#include "WinHandle.hpp"
#include "Security.hpp"
#include <TlHelp32.h>

using namespace win32;

void process::for_each(const std::function<bool(const PROCESSENTRY32W&)>& cb) {
    unique_handle snap(::CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0));
    if (!snap) return;

    PROCESSENTRY32W pe{sizeof pe};
    if (!::Process32FirstW(snap.get(), &pe)) return;

    do {
        if (cb(pe)) break;
    } while (::Process32NextW(snap.get(), &pe));
}

bool process::find_by_sid(const std::wstring& sid, DWORD& pid) {
    pid = 0;
    for_each([&](const PROCESSENTRY32W& pe) {
        if (security::process_matches_sid(pe.th32ProcessID, sid)) {
            pid = pe.th32ProcessID;
            return true;
        }
        return false;
    });
    return pid != 0;
}
