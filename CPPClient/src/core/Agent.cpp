#include "Agent.h"
#include <iostream>

using namespace CppAgent;

Agent::Agent()
    : client_(std::string("ws://") + Config::SERVER_IP + ":" + std::to_string(Config::SERVER_PORT))
{
    initLogger(true, true, Config::LOG_FILE);
}

bool Agent::run() {
    auto& logger = getLogger();
    logger.log("========== " + std::string(Config::AGENT_NAME) + " ==========", Logger::Level::Info);
    logger.log("Attempting connection to: " + client_.get_uri(), Logger::Level::Info);

    if (!client_.start()) {
        logger.log("Failed to start WebSocket session.", Logger::Level::Error);
        return false;
    }
    logger.log("Session started. Press Enter to exit...", Logger::Level::Info);
    std::cin.get();
    client_.stop();
    logger.log("Connection closed.", Logger::Level::Info);
    return true;
}
