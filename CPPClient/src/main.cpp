#include <iostream>
#include "Logger/GlobalLogger.h"
#include "Config.h"
#include "WsClient/WsClient.h"

int main() {
    CppAgent::Config config;
    CppAgent::initLogger(true, true, config.LOG_FILE);
    auto& logger = CppAgent::getLogger();

    // Start of agent
    logger.log("========== " + std::string(config.AGENT_NAME) + " ==========", CppAgent::Logger::Level::Info);
    logger.log("Initializing agent configuration...", CppAgent::Logger::Level::Info);

    // WebSocket URI creation
    std::string uri = std::string("ws://") + config.SERVER_IP + ":" + std::to_string(config.SERVER_PORT) + "/" + config.AGENT_ID;
    logger.log("Attempting connection to: " + uri, CppAgent::Logger::Level::Info);

    // Initialize WebSocket client
    CppAgent::WsClient client(uri);
    logger.log("WebSocket client initialized.", CppAgent::Logger::Level::Info);

    // Start WebSocket connection
    if (client.start()) {
        logger.log("Session successfully started.", CppAgent::Logger::Level::Info);
    }
    else {
        logger.log("Failed to start WebSocket session.", CppAgent::Logger::Level::Error);
        return 1; // Return early if critical connection fails
    }

    // Run until user stops
    logger.log("Agent running. Awaiting shutdown signal (press Enter)...", CppAgent::Logger::Level::Info);
    std::cin.get();

    // Graceful shutdown
    logger.log("Shutdown signal received. Closing connection...", CppAgent::Logger::Level::Info);
    client.stop();
    logger.log("Connection closed. Exiting gracefully.", CppAgent::Logger::Level::Info);

    return 0;
}
