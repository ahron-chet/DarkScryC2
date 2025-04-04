#include "pch.h"
#include <TlHelp32.h>
#include "sddl.h"

static bool EnablePrivilege(const wchar_t* priv) {
    HANDLE hToken = nullptr;
    if (!OpenProcessToken(GetCurrentProcess(), TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY, &hToken)) return false;
    LUID luid;
    if (!LookupPrivilegeValueW(nullptr, priv, &luid)) {
        CloseHandle(hToken);
        return false;
    }
    TOKEN_PRIVILEGES tp{};
    tp.PrivilegeCount = 1;
    tp.Privileges[0].Luid = luid;
    tp.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED;
    bool ok = AdjustTokenPrivileges(hToken, false, &tp, sizeof(tp), nullptr, nullptr);
    CloseHandle(hToken);
    return ok;
}

Shell::Shell() : running(false), hStdoutRead(nullptr), hStdinWrite(nullptr) {
    RtlZeroMemory(&processInfo, sizeof(processInfo));
    RtlZeroMemory(&startupInfo, sizeof(startupInfo));
    startupInfo.cb = sizeof(startupInfo);
}

Shell::~Shell() {
    Stop();
    CloseHandle(hStdinWrite);
    CloseHandle(processInfo.hProcess);
    CloseHandle(processInfo.hThread);
    if (outputThread.joinable()) outputThread.join();
}

bool Shell::FindProcessBySid(const std::wstring& sidString, DWORD& outPid) {
    outPid = 0;
    HANDLE snap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (snap == INVALID_HANDLE_VALUE) return false;
    PROCESSENTRY32W pe{};
    pe.dwSize = sizeof(pe);
    if (Process32FirstW(snap, &pe)) {
        do {
            if (IsProcessMatchingSid(pe.th32ProcessID, sidString)) {
                outPid = pe.th32ProcessID;
                break;
            }
        } while (Process32NextW(snap, &pe));
    }
    CloseHandle(snap);
    return (outPid != 0);
}

bool Shell::IsProcessMatchingSid(DWORD pid, const std::wstring& sidString) {
    HANDLE hProc = OpenProcess(PROCESS_QUERY_INFORMATION, FALSE, pid);
    if (!hProc) return false;

    HANDLE hTok = nullptr;
    if (!OpenProcessToken(hProc, TOKEN_QUERY, &hTok)) {
        CloseHandle(hProc);
        return false;
    }
    CloseHandle(hProc);

    DWORD len = 0;
    GetTokenInformation(hTok, TokenUser, nullptr, 0, &len);
    if (GetLastError() != ERROR_INSUFFICIENT_BUFFER) {
        CloseHandle(hTok);
        return false;
    }
    PTOKEN_USER ptu = (PTOKEN_USER)HeapAlloc(GetProcessHeap(), HEAP_ZERO_MEMORY, len);
    if (!ptu) {
        CloseHandle(hTok);
        return false;
    }
    bool result = false;
    if (GetTokenInformation(hTok, TokenUser, ptu, len, &len)) {
        LPWSTR stringSid = nullptr;
        if (ConvertSidToStringSidW(ptu->User.Sid, &stringSid)) {
            if (_wcsicmp(stringSid, sidString.c_str()) == 0) {
                result = true;
            }
            LocalFree(stringSid);
        }
    }
    HeapFree(GetProcessHeap(), 0, ptu);
    CloseHandle(hTok);
    return result;
}

bool Shell::CreateShellInstanceBySid(const std::wstring& sidString) {
    SECURITY_ATTRIBUTES sa{};
    sa.nLength = sizeof(sa);
    sa.bInheritHandle = TRUE;

    HANDLE hStdoutWrite, hStdinRead;
    if (!CreatePipe(&hStdoutRead, &hStdoutWrite, &sa, 0)) return false;
    if (!CreatePipe(&hStdinRead, &hStdinWrite, &sa, 0)) return false;

    startupInfo.dwFlags = STARTF_USESTDHANDLES;
    startupInfo.hStdOutput = hStdoutWrite;
    startupInfo.hStdError = hStdoutWrite;
    startupInfo.hStdInput = hStdinRead;

    RtlZeroMemory(&processInfo, sizeof(processInfo));

    if (_wcsicmp(sidString.c_str(), L"CURRENT_USER") == 0) {
        // Just create a normal cmd.exe in the current user context
        if (!CreateProcessW(
            L"C:\\Windows\\System32\\cmd.exe",
            nullptr,
            nullptr,
            nullptr,
            TRUE,
            CREATE_NO_WINDOW,
            nullptr,
            nullptr,
            &startupInfo,
            &processInfo))
        {
            return false;
        }
    }
    else {
        // Need SeDebugPrivilege to open another process token
        if (!EnablePrivilege(L"SeDebugPrivilege")) {
            return false;
        }
        DWORD pid = 0;
        if (!FindProcessBySid(sidString, pid) || !pid) {
            return false;
        }
        HANDLE hProc = OpenProcess(PROCESS_QUERY_INFORMATION, FALSE, pid);
        if (!hProc) {
            return false;
        }
        HANDLE hTok = nullptr;
        if (!OpenProcessToken(hProc, TOKEN_DUPLICATE | TOKEN_ASSIGN_PRIMARY | TOKEN_QUERY, &hTok)) {
            CloseHandle(hProc);
            return false;
        }
        CloseHandle(hProc);

        HANDLE hDup = nullptr;
        if (!DuplicateTokenEx(hTok, MAXIMUM_ALLOWED, nullptr, SecurityIdentification, TokenPrimary, &hDup)) {
            CloseHandle(hTok);
            return false;
        }
        CloseHandle(hTok);

        if (!CreateProcessWithTokenW(
            hDup,
            0,
            L"C:\\Windows\\System32\\cmd.exe",
            nullptr,
            CREATE_NO_WINDOW,
            nullptr,
            nullptr,
            &startupInfo,
            &processInfo))
        {
            CloseHandle(hDup);
            return false;
        }
        CloseHandle(hDup);
    }
    return true;
}

void Shell::DoOutput(std::function<void(const char*)> func) {
    char buf[4096];
    while (running) {
        DWORD readBytes = 0;
        if (!ReadFile(hStdoutRead, buf, 4095, &readBytes, nullptr) || readBytes == 0) {
            break;
        }
        buf[readBytes] = '\0';
        func(buf);
    }
}

void Shell::Start(std::function<void(const char*)> outputHandler) {
    if (running) return;
    running = true;
    outputThread = std::thread(&Shell::DoOutput, this, outputHandler);
}

void Shell::SendCommand(const std::string& cmd) {
    std::string line = cmd + "\n";
    WriteFile(hStdinWrite, line.c_str(), (DWORD)line.size(), nullptr, nullptr);
}

void Shell::Stop() {
    if (running) {
        running = false;
        SendCommand("exit");
        TerminateProcess(processInfo.hProcess, 0);
        CloseHandle(hStdoutRead);
        if (outputThread.joinable()) {
            outputThread.join();
        }
    }
}


// Simple RAII wrapper or direct usage:
extern "C" {

    SHELLDLL_API void* CreateShellInstanceBySid(const std::wstring& sidString)
    {
        try {
            Shell* sh = new Shell();
            sh->CreateShellInstanceBySid(sidString);
            return sh;
        }
        catch (...) {
            return nullptr;
        }
    }

    SHELLDLL_API void DestroyShellInstance(void* shellInstance)
    {
        if (!shellInstance) return;
        Shell* shell = static_cast<Shell*>(shellInstance);
        delete shell;
    }

    SHELLDLL_API void StartShell(void* shellInstance, ShellOutputCallback cb)
    {
        if (!shellInstance) return;
        Shell* shell = static_cast<Shell*>(shellInstance);


        shell->Start([cb](const char* output) {
            if (cb) {
                cb(output);
            }
            });
    }

    SHELLDLL_API void SendShellCommand(void* shellInstance, const char* command)
    {
        if (!shellInstance) return;
        Shell* shell = static_cast<Shell*>(shellInstance);
        shell->SendCommand(command);
    }

    SHELLDLL_API void StopShell(void* shellInstance)
    {
        if (!shellInstance) return;
        Shell* shell = static_cast<Shell*>(shellInstance);
        shell->Stop();
    }

} // extern "C"
