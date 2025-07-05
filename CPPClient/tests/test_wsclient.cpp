#include "WsClient/WsClient.h"
#include "Logger/Logger.h"
#include <gtest/gtest.h>

TEST(WsClientTest, CanConstruct) {
    CppAgent::Logger logger(false, false);
    CppAgent::WsClient client("ws://localhost:12345/test", logger);
    SUCCEED();
}

