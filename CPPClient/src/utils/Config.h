#pragma once
#include <string>

namespace CppAgent {
    struct Config {
        static constexpr const char* AGENT_ID = "004ce4c4-1af4-4abb-aa6b-57ac9cc0d5ce";
        static constexpr const char* SERVER_IP = "127.0.0.1";
        static constexpr unsigned short SERVER_PORT = 876; // WebSocket port
        static constexpr const char* AGENT_NAME = "DarkScry C++ Agent";
		static constexpr const char* LOG_FILE = "agent.log";
    };
}
