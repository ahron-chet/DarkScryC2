#pragma once
#include <rapidjson/document.h>

namespace CppAgent::serialization {

template<class Info>
rapidjson::Value toJson(const Info& src,
                        rapidjson::Document::AllocatorType& a)
{
    using rapidjson::Value;
    Value o(rapidjson::kObjectType);

    auto s = [&](const std::string& v) { return Value(v.c_str(), static_cast<rapidjson::SizeType>(v.size()), a); };

    o.AddMember("HostName",         s(src.host_name),         a);
    o.AddMember("OperatingSystem",  s(src.operating_system),  a);
    o.AddMember("OSVersionDetail",  s(src.os_version_detail), a);
    o.AddMember("CPU",              s(src.cpu),               a);
    o.AddMember("RAM",              s(src.ram),               a);
    o.AddMember("Disk",             s(src.disk),              a);
    o.AddMember("PrimaryIP",        s(src.primary_ip),        a);
    o.AddMember("GPU",              s(src.gpu),               a);
    o.AddMember("AgentStatus",      s("Active and Monitoring"), a);

    o.AddMember("LastLogin",
                s(src.logged_on_sessions.empty() ? "" : src.logged_on_sessions.front()),
                a);

    Value sessions(rapidjson::kArrayType);
    for (auto& user : src.logged_on_sessions)
        sessions.PushBack(s(user), a);
    o.AddMember("LoggedInSessions", sessions, a);

    return o;
}

} // namespace CppAgent::serialization
