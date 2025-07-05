#include "Logger/Logger.h"
#include <gtest/gtest.h>
#include <fstream>
#include <cstdio>

TEST(LoggerTest, WritesToFile) {
    const char* logPath = "test.log";
    std::remove(logPath);

    CppAgent::Logger logger(false, true, logPath);
    std::string msg = "sample message";
    logger.log(msg, CppAgent::Logger::Level::Info);

    std::ifstream file(logPath);
    ASSERT_TRUE(file.is_open());

    std::string line;
    std::getline(file, line);
    file.close();

    EXPECT_NE(line.find(msg), std::string::npos);
}

