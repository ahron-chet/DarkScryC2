#include <iostream>
#include "Logger.h"
#include "DarkScryCpp/Config.h"
#include "WsClient/WsClient.h"

int main() {
    CppAgent::Config config;
    CppAgent::Logger logger(true, true, config.LOG_FILE);
    logger.log(std::string(config.AGENT_NAME) + " started", CppAgent::Logger::Level::Info);

    std::string uri = std::string("ws://") + config.SERVER_IP + ":" + std::to_string(config.SERVER_PORT) + "/" + config.AGENT_ID;
    CppAgent::WsClient client(uri, logger);
    if (client.start()) {
        logger.log("Session started", CppAgent::Logger::Level::Info);
    } else {
        logger.log("Failed to start session", CppAgent::Logger::Level::Error);
    }

    // Run until user stops
    std::cout << "Press enter to exit..." << std::endl;
    std::cin.get();

    client.stop();
    return 0;
}
