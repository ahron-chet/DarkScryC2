#pragma once
#include <string>

namespace CppAgent {
    struct Config {
        static constexpr const char* AGENT_ID = "95a0f517-714f-4995-8a08-f54a531e75e4";
        static constexpr const char* SERVER_IP = "172.236.98.55";
        static constexpr unsigned short SERVER_PORT = 876; // WebSocket port
        static constexpr const char* AGENT_NAME = "DarkScry C++ Agent";
		static constexpr const char* LOG_FILE = "agent.log";
    };
}
