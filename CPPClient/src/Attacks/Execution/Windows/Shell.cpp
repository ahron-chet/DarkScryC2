#include "Shell.hpp"  
#include <array>  
#include <random>  
#include <sstream>  
#include <algorithm>   
#include "Logger/GlobalLogger.h"
#include "win32/include/ProcessLauncher.hpp"
#include "win32/include/UserUtils.hpp"
#include "win32/include/WinUtils.hpp"
#include "GeneralUtils.hpp"

using namespace win32;
using namespace win32::security;
using namespace win32::process;
using namespace CppAgent;

Shell::Shell() {}
Shell::~Shell() { stop(); }

bool Shell::create_by_sid(const std::wstring& sid)
{
    if (is_running()) {
        if (utils::iequals(current_sid_, sid)) {
            DARKSCRY_LOG("Shell session already running for SID: "
                         + win32::narrow(sid), Logger::Level::Debug);
            return true;
        }
        stop();
    }

    // ── 1. Build anonymous pipes
    SECURITY_ATTRIBUTES sa{ sizeof sa, nullptr, TRUE };
    HANDLE r{}, w{}, ir{}, iw{};
    if (!::CreatePipe(&r, &w, &sa, 0) || !::CreatePipe(&ir, &iw, &sa, 0))
        return false;

    out_rd_.reset(r);  out_wr_.reset(w);
    in_rd_.reset(ir);  in_wr_.reset(iw);

    // ── 2. Fill STARTUPINFO via LaunchOptions
    LaunchOptions opt = LaunchOptions::impersonate_sid(sid);
    opt.si.cb         = sizeof(opt.si);
    opt.si.dwFlags    = STARTF_USESTDHANDLES;
    opt.si.hStdOutput = out_wr_.get();
    opt.si.hStdError  = out_wr_.get();
    opt.si.hStdInput  = in_rd_.get();

    // ── 3. Ask the helper to launch the process
    if (!launch(opt))
        return false;
    pi_ = opt.pi;

    current_sid_ = sid;
    return true;
}

void Shell::write_line(std::string_view sv) {  
   std::string s(sv);  
   s.push_back('\n');  
   DWORD wr{};  
   ::WriteFile(in_wr_.get(), s.data(), static_cast<DWORD>(s.size()), &wr, nullptr);  
}  

std::string Shell::read_line() {  
   std::string s; char ch; DWORD rd{};  
   while (::ReadFile(out_rd_.get(), &ch, 1, &rd, nullptr) && rd == 1) {  
       if (ch == '\r') continue;  
       if (ch == '\n') break;  
       s.push_back(ch);  
   }  
   return s;  
}  

void Shell::flush_pipe() {  
   constexpr DWORD BUF = 4096; char buf[BUF]; DWORD avail{}, rd{};  
   while (::PeekNamedPipe(out_rd_.get(), nullptr, 0, nullptr, &avail, nullptr) && avail)  
       ::ReadFile(out_rd_.get(), buf, std::min<DWORD>(avail, BUF), &rd, nullptr);  
}  

std::string Shell::make_sentinel() {  
   static std::mt19937_64 rng{std::random_device{}()};  
   std::ostringstream oss; oss << "__SENTINEL_" << std::hex << rng() << "__";  
   return oss.str();  
}  

std::string Shell::run_command(std::string_view cmd) {  
   if (running_) throw std::logic_error("run_command while streaming");  

   if (!echo_off_) { write_line("@echo off"); read_line(); echo_off_ = true; }  

   flush_pipe();  

   const std::string actual   = std::string(cmd) + " 2>&1";  
   const std::string sentinel = "echo " + make_sentinel();  

   write_line(actual);  
   write_line(sentinel);  

   std::ostringstream out;  
   bool echoed = false;  

   for (;;) {  
       std::string line = read_line();  
       if (line.starts_with(sentinel)) break;  
       if (!echoed && line.find(actual) != std::string::npos) { echoed = true; continue; }  
       out << line << '\n';  
   }  

   std::string res = out.str();  
   if (!res.empty() && res.back() == '\n') res.pop_back();  
   return res;  
}  

void Shell::thread_loop(const std::function<void(const char*)>& cb) {  
   std::array<char, 4096> buf{};  
   while (running_) {  
       DWORD rd{};  
       if (!::ReadFile(out_rd_.get(), buf.data(), buf.size() - 1, &rd, nullptr) || rd == 0)  
           break;  
       buf[rd] = '\0';  
       cb(buf.data());  
   }  
}  

void Shell::start(const std::function<void(const char*)>& cb) {  
   if (running_) return;  
   running_ = true;  
   th_ = std::thread(&Shell::thread_loop, this, cb);  
}  

void Shell::send(std::string_view cmd) { write_line(cmd); }  

void Shell::stop() {
   if (!pi_.hProcess) return;
   if (running_) {
       running_ = false; write_line("exit");
       if (th_.joinable()) th_.join();
   }
   ::TerminateProcess(pi_.hProcess, 0);
   ::CloseHandle(pi_.hThread);
   ::CloseHandle(pi_.hProcess);
   pi_ = {};
   out_rd_.reset(); out_wr_.reset();
   in_rd_.reset(); in_wr_.reset();
   current_sid_.clear();
   echo_off_ = false;
}
