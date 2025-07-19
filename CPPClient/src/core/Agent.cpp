#include "Agent.h"
#include <iostream>

using namespace CppAgent;

Agent::Agent()
    : client_(std::string("ws://") + Config::SERVER_IP + ":" +
        std::to_string(Config::SERVER_PORT) + "/" + Config::AGENT_ID)
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

    try {
        logger.log("Session started. Waiting until connection closes...", Logger::Level::Info);

        client_.wait_close();
    }
    catch (const std::exception& e) {
        logger.log(std::string("Exception occurred: ") + e.what(), Logger::Level::Error);
    }
    catch (...) {
        logger.log("Unknown exception occurred.", Logger::Level::Error);
    }

    client_.stop();
    logger.log("Connection closed.", Logger::Level::Info);

    return true;
}

