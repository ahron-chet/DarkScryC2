#pragma once  
#include <Windows.h>  
#include <atomic>
#include <functional>
#include <string_view>
#include <thread>

#include "win32/include/WinHandle.hpp"
#include "ShellLaunchDesc.hpp"

namespace win32 {  

class Shell {  
public:
   Shell();
   ~Shell();

    /// Create a cmd.exe session according to `desc`.
    bool        create(const ShellLaunchDesc& desc);
    bool is_running() const { return pi_.hProcess != nullptr; }

   std::string run_command(std::string_view cmd);  
   void start(const std::function<void(const char*)>& cb);  
   void send(std::string_view cmd);  
   void stop();  

   Shell(const Shell&) = delete;  
   Shell& operator=(const Shell&) = delete;  

private:  
   void write_line(std::string_view sv);  
   std::string read_line();  
   void flush_pipe();  
   std::string make_sentinel();  
   void thread_loop(const std::function<void(const char*)>& cb);  

    unique_handle       out_rd_, out_wr_, in_rd_, in_wr_;
    PROCESS_INFORMATION pi_{};
    std::thread         th_;
    std::atomic_bool    running_{false};
    bool                echo_off_{false};
};

} // namespace win32
