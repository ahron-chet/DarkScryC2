#pragma once 
#define NOMINMAX
#include <string>  
#include <memory>  
#include <Execution/Shell.hpp>




namespace CppAgent {
    class CommandHandler {
    public:
        CommandHandler();
        std::string handle(const std::string& commandJson);
private:
        bool shell_running_;
        std::unique_ptr<execution::Shell> shell_;
        enum CommandIdentifier {
            START_SHELL_INSTANCE = 1,
            RUN_COMMAND = 2,
            GET_BASIC_MACHINE_INFO = 3
        };
    };
}
