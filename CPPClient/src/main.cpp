#include <iostream>
#include "Logger/GlobalLogger.h"
#include "Config.h"
#include "WsClient/WsClient.h"

int main() {
    CppAgent::Config config;
    CppAgent::initLogger(true, true, config.LOG_FILE);
    auto& logger = CppAgent::getLogger();

    int exitCode = 0; // Default to success

    logger.log("========== " + std::string(config.AGENT_NAME) + " ==========", CppAgent::Logger::Level::Info);
    logger.log("Initializing agent configuration...", CppAgent::Logger::Level::Info);

    std::string uri = "ws://" + std::string(config.SERVER_IP) + ":" + std::to_string(config.SERVER_PORT); //+ "/" + config.AGENT_ID;
    logger.log("Attempting connection to: " + uri, CppAgent::Logger::Level::Info);

    CppAgent::WsClient client(uri);
    logger.log("WebSocket client initialized.", CppAgent::Logger::Level::Info);

    if (!client.start()) {
        logger.log("Failed to start WebSocket session.", CppAgent::Logger::Level::Error);
        exitCode = 1;
        goto cleanup;
    }
    logger.log("Session successfully started.", CppAgent::Logger::Level::Info);

    if (!client.send("Hello from C++ Agent!")) {
        logger.log("Failed to send initial message.", CppAgent::Logger::Level::Error);
        exitCode = 2;
        goto cleanup;
    }

    logger.log("Agent running. Awaiting shutdown signal (press Enter)...", CppAgent::Logger::Level::Info);
    std::cin.get();

cleanup:
    logger.log("Shutdown initiated. Closing connection...", CppAgent::Logger::Level::Info);
    client.stop();
    logger.log("Connection closed. Exiting gracefully.", CppAgent::Logger::Level::Info);

    return exitCode;
}
