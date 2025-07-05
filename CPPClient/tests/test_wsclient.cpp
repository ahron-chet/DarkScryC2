#include "WsClient/WsClient.h"
#include "Logger/GlobalLogger.h"
#include <gtest/gtest.h>

TEST(WsClientTest, CanConstruct) {
    CppAgent::initLogger();
    CppAgent::WsClient client("ws://localhost:12345/test");
    SUCCEED();
}

