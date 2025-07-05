#pragma once
#include "Logger.h"
#include <memory>

namespace CppAgent {
    void initLogger(bool toConsole = false, bool toFile = false, const std::string& path = "log.txt");
    Logger& getLogger();
}
