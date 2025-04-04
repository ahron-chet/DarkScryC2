#pragma once

// #ifdef SHELLDLL_EXPORTS
// #define SHELLDLL_API __declspec(dllexport)
// #else
// #define SHELLDLL_API __declspec(dllimport)
// #endif

#define SHELLDLL_API __declspec(dllexport)


class Shell {
public:
    Shell();
    ~Shell();
    bool CreateShellInstanceBySid(const std::wstring& sidString);
    void Start(std::function<void(const char*)> outputHandler);
    void SendCommand(const std::string& command);
    void Stop();
private:
    void DoOutput(std::function<void(const char*)> func);
    bool FindProcessBySid(const std::wstring& sidString, DWORD& outPid);
    bool IsProcessMatchingSid(DWORD pid, const std::wstring& sidString);

private:
    HANDLE hStdoutRead;
    HANDLE hStdinWrite;
    PROCESS_INFORMATION processInfo;
    STARTUPINFOW startupInfo;
    std::thread outputThread;
    bool running;
};

extern "C" {
    typedef void(__stdcall* ShellOutputCallback)(const char*);

    // Create instance of the Shell class
    SHELLDLL_API void* CreateShellInstanceBySid(const std::wstring& sidString);

    // Destroy instance of the Shell class
    SHELLDLL_API void DestroyShellInstance(void* shellInstance);

    // Start reading output, pass callback pointer
    SHELLDLL_API void StartShell(void* shellInstance, ShellOutputCallback cb);

    // Send command
    SHELLDLL_API void SendShellCommand(void* shellInstance, const char* command);

    // Stop the shell
    SHELLDLL_API void StopShell(void* shellInstance);
}
