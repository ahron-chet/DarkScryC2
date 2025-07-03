#include "Config.h"
#include "NetworkClient.h"
#include "Logger.h"
#include <string>
#include <chrono>
#include <thread>

using namespace CppAgent;

int wmain() {
    Logger log(true, false);
    NetworkClient client(log);

    std::string uri = "ws://" + std::string(Config::SERVER_IP) + ":" + std::to_string(Config::SERVER_PORT) + "/" + std::string(Config::AGENT_ID);
    log.log("Connecting to " + uri);
    if (!client.connect(uri)) {
        log.log("Failed to connect to server", Logger::Level::Error);
        return 1;
    }

    client.set_message_handler([&](const std::string& msg){
        log.log("Received: " + msg, Logger::Level::Debug);
        client.send(msg); // echo
    });

    // keep running until connection closes
    while (true) {
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }

    return 0;
}
