#pragma once
#include <string>
#include <string_view>
#include <thread>
#include <functional>
#include <atomic>
#include <sys/types.h>

namespace linux_os {

class Shell {
public:
    Shell();
    ~Shell();

    bool create();

    std::string get_current_sid() const { return {}; }

    std::string run_command(std::string_view cmd);
    void start(const std::function<void(const char*)>& cb);
    void send(std::string_view cmd);
    void stop();

    Shell(const Shell&) = delete;
    Shell& operator=(const Shell&) = delete;

private:
    void thread_loop(const std::function<void(const char*)>& cb);

    int in_fd_{-1};
    int out_fd_{-1};
    pid_t pid_{-1};
    std::thread th_;
    std::atomic_bool running_{false};
};

} // namespace linux_os
