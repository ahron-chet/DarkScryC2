#include "CommandHandler/CommandHandler.h"
#include "Logger/GlobalLogger.h"
#include <gtest/gtest.h>

TEST(CommandHandlerTest, ReturnsOutput) {
    CppAgent::initLogger();
    CppAgent::CommandHandler handler;
    std::string cmd = "{\"action\":1}";
    EXPECT_EQ(handler.handle(cmd), "output");
    std::string cmd2 = "{\"action\":2,\"command\":\"dir\"}";
    EXPECT_EQ(handler.handle(cmd2), "output");
}
