#pragma once
#include <string>
#include <fstream>
#include <mutex>

namespace CppAgent {
    class Logger {
    public:
        enum class Level { Info, Debug, Warning, Error, Critical };

        Logger(bool toConsole = false, bool toFile = false, const std::string& path = "log.txt");
        ~Logger();

        void log(const std::string& message, Level level = Level::Info);

    private:
        std::ofstream file_;
        bool console_;
        bool fileOut_;
        std::mutex mtx_;

        std::string format(const std::string& msg, Level level);
        void writeConsole(const std::string& msg, Level level);
    };
}
