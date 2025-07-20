#pragma once  
#include <Windows.h>  
#include <string>  
#include <string_view>  
#include <thread>  
#include <functional>  
#include <atomic>  
#include "win32/include/WinHandle.hpp" 
#include "win32/include/Process.hpp"

namespace win32 {  

class Shell {  
public:  
   Shell();  
   ~Shell();  

   bool create_by_sid(const std::wstring& sid = L"CURRENT_USER");  

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
   STARTUPINFOW        si_{};  
   std::thread         th_;  
   std::atomic_bool    running_{false};  
   bool                echo_off_{false};  
};  

} // namespace win32
