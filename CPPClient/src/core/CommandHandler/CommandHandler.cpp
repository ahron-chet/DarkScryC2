#include "CommandHandler.h"
#include "Logger/GlobalLogger.h"
#include <algorithm>
#include <rapidjson/document.h>

using namespace CppAgent;

CommandHandler::CommandHandler() : shell_running_(false) {}

std::string CommandHandler::handle(const std::string& commandJson) {
    rapidjson::Document doc;
    if (doc.Parse(commandJson.c_str()).HasParseError() || !doc.IsObject()) {
        getLogger().log("Invalid JSON", Logger::Level::Warning);
        return "";
    }

    if (!doc.HasMember("action") || !doc["action"].IsInt()) {
        getLogger().log("No action provided", Logger::Level::Warning);
        return "";
    }

    int action = doc["action"].GetInt();

    if (action == START_SHELL_INSTANCE) {
        shell_running_ = true;
        getLogger().log("Start shell instance requested", Logger::Level::Info);
        return "output";
    } else if (action == RUN_COMMAND) {
        if (!shell_running_) {
            getLogger().log("Run command but shell not running", Logger::Level::Warning);
            return "output";
        }
        if (doc.HasMember("command") && doc["command"].IsString()) {
            std::string cmd = doc["command"].GetString();
            getLogger().log("Run command: " + cmd, Logger::Level::Debug);
        }
        return "output";
    }

    getLogger().log("Unknown action: " + std::to_string(action), Logger::Level::Warning);
    return "output";
}

