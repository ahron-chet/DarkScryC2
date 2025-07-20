#include "Shell.hpp"
#include <unistd.h>
#include <sys/wait.h>
#include <signal.h>
#include <cstdio>
#include <cstring>

using namespace linux_os;

Shell::Shell() = default;
Shell::~Shell() { stop(); }

bool Shell::create() {
    int in_pipe[2];
    int out_pipe[2];
    if (pipe(in_pipe) == -1 || pipe(out_pipe) == -1)
        return false;

    pid_ = fork();
    if (pid_ < 0)
        return false;

    if (pid_ == 0) {
        dup2(in_pipe[0], STDIN_FILENO);
        dup2(out_pipe[1], STDOUT_FILENO);
        dup2(out_pipe[1], STDERR_FILENO);
        close(in_pipe[0]);
        close(in_pipe[1]);
        close(out_pipe[0]);
        close(out_pipe[1]);
        execl("/bin/sh", "sh", nullptr);
        _exit(1);
    }

    close(in_pipe[0]);
    close(out_pipe[1]);
    in_fd_ = in_pipe[1];
    out_fd_ = out_pipe[0];
    return true;
}

std::string Shell::run_command(std::string_view cmd) {
    std::string s(cmd);
    FILE* pipe = popen(("/bin/sh -c '" + s + "' 2>&1").c_str(), "r");
    if (!pipe) return {};
    char buffer[256];
    std::string result;
    while (fgets(buffer, sizeof(buffer), pipe)) {
        result += buffer;
    }
    pclose(pipe);
    if (!result.empty() && result.back() == '\n')
        result.pop_back();
    return result;
}

void Shell::thread_loop(const std::function<void(const char*)>& cb) {
    char buf[4096];
    while (running_) {
        ssize_t rd = read(out_fd_, buf, sizeof(buf) - 1);
        if (rd <= 0) break;
        buf[rd] = '\0';
        cb(buf);
    }
}

void Shell::start(const std::function<void(const char*)>& cb) {
    if (running_) return;
    running_ = true;
    th_ = std::thread(&Shell::thread_loop, this, cb);
}

void Shell::send(std::string_view cmd) {
    std::string s(cmd);
    s.push_back('\n');
    write(in_fd_, s.data(), s.size());
}

void Shell::stop() {
    if (pid_ == -1) return;
    if (running_) {
        running_ = false;
        write(in_fd_, "exit\n", 5);
        if (th_.joinable()) th_.join();
    }
    kill(pid_, SIGTERM);
    waitpid(pid_, nullptr, 0);
    close(in_fd_);
    close(out_fd_);
    pid_ = -1;
    in_fd_ = -1;
    out_fd_ = -1;
}

