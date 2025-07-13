#pragma once

#include "WsClient/WsClient.h"
#include "Logger/GlobalLogger.h"
#include "Config.h"

namespace CppAgent {
    // Main agent orchestrating communication and command execution
    class Agent {
    public:
        Agent();
        // Run the agent. Returns true on clean shutdown
        bool run();
    private:
        WsClient client_;
    };
}
