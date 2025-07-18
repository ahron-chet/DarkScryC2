#include "CommandHandler/CommandHandler.h"
#include "Logger/GlobalLogger.h"
#include <rapidjson/document.h>
#include <gtest/gtest.h>

TEST(CommandHandlerTest, ReturnsJson) {
    CppAgent::initLogger();
    CppAgent::CommandHandler handler;
    std::string cmd = "{\"action\":1}";
    auto resp1 = handler.handle(cmd);
    rapidjson::Document d1;
    d1.Parse(resp1.c_str());
    ASSERT_TRUE(d1.IsObject());
    EXPECT_TRUE(d1["success"].GetBool());

    std::string cmd2 = "{\"action\":2,\"command\":\"dir\"}";
    auto resp2 = handler.handle(cmd2);
    rapidjson::Document d2;
    d2.Parse(resp2.c_str());
    ASSERT_TRUE(d2.IsObject());
    EXPECT_TRUE(d2["success"].GetBool());
}
