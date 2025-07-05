#pragma once
#include <string>

namespace CppAgent {
    class CommandHandler {
    public:
        CommandHandler();
        std::string handle(const std::string& commandJson);
    private:
        bool shell_running_;
        static constexpr int START_SHELL_INSTANCE = 1;
        static constexpr int RUN_COMMAND = 2;
    };
}
