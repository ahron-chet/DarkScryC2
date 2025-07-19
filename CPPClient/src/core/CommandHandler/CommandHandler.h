#pragma once 
#define NOMINMAX
#include <string>  
#include <memory>  
#ifdef _WIN32
#include <execution/shell_service/Shell.hpp>
#else
#include <execution/linux_shell_service/Shell.hpp>
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
#else
        std::unique_ptr<linux_os::Shell> shell_;
#endif
        enum CommandIdentifier {
            START_SHELL_INSTANCE = 1,
            RUN_COMMAND = 2,
            GET_BASIC_MACHINE_INFO = 3
        };
    };
}
