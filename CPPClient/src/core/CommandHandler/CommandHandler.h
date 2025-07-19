#pragma once 
#define NOMINMAX
#include <string>  
#include <memory>  
#include "shell_service/Shell.hpp"



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
        enum CommandIdentifier {
            START_SHELL_INSTANCE = 1,
            RUN_COMMAND = 2
        };
    };
}
