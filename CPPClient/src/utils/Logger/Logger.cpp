#include "Logger.h"
#include "GlobalLogger.h"
#include <chrono>
#include <ctime>
#include <iostream>
#ifdef _WIN32
#include <windows.h>
#endif

using namespace CppAgent;

Logger::Logger(bool toConsole, bool toFile, const std::string& path)
    : console_(toConsole), fileOut_(toFile) {
    if (fileOut_) {
        file_.open(path, std::ios::app);
    }
}

Logger::~Logger() {
    if (file_.is_open()) file_.close();
}

void Logger::log(const std::string& message, Level level) {
    std::lock_guard<std::mutex> lock(mtx_);
    std::string formatted = format(message, level);
    if (console_) {
        writeConsole(formatted, level);
    }
    if (fileOut_ && file_.is_open()) {
        file_ << formatted << std::endl;
    }
}

std::string Logger::format(const std::string& msg, Level level) {
    auto now = std::chrono::system_clock::to_time_t(std::chrono::system_clock::now());
    char buf[64];
    std::strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S", std::localtime(&now));
    std::string lvl;
    switch (level) {
    case Level::Info: lvl = "INFO"; break;
    case Level::Debug: lvl = "DEBUG"; break;
    case Level::Warning: lvl = "WARN"; break;
    case Level::Error: lvl = "ERROR"; break;
    case Level::Critical: lvl = "CRITICAL"; break;
    }
    return std::string("[") + buf + "] [" + lvl + "] " + msg;
}

void Logger::writeConsole(const std::string& msg, Level level) {
#ifdef _WIN32
    HANDLE h = GetStdHandle(STD_OUTPUT_HANDLE);
    WORD color = FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE;
    switch (level) {
    case Level::Warning:
        color = FOREGROUND_RED | FOREGROUND_GREEN;
        break;
    case Level::Error:
    case Level::Critical:
        color = FOREGROUND_RED;
        break;
    default:
        color = FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE;
        break;
    }
    SetConsoleTextAttribute(h, color);
    std::cout << msg << std::endl;
    SetConsoleTextAttribute(h, FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE);
#else
    std::cout << msg << std::endl;
#endif
}

namespace CppAgent {
    namespace {
        std::unique_ptr<Logger> globalLogger;
    }

    void initLogger(bool toConsole, bool toFile, const std::string& path) {
        globalLogger = std::make_unique<Logger>(toConsole, toFile, path);
    }

    Logger& getLogger() {
        if (!globalLogger) {
            globalLogger = std::make_unique<Logger>();
        }
        return *globalLogger;
    }
}
