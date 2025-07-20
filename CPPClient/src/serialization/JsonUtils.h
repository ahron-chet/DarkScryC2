#pragma once
#include <string>
#include <rapidjson/document.h>

namespace CppAgent::json {

/// Convenience wrappers – keep them tiny & inline.
/// Return *true* on success; leave `out` untouched otherwise.
inline bool getInt (const rapidjson::Value& obj, const char* key, int& out)
{
    auto it = obj.FindMember(key);
    if (it != obj.MemberEnd() && it->value.IsInt()) {
        out = it->value.GetInt();
        return true;
    }
    return false;
}

inline bool getString(const rapidjson::Value& obj, const char* key, std::string& out)
{
    auto it = obj.FindMember(key);
    if (it != obj.MemberEnd() && it->value.IsString()) {
        out = it->value.GetString();
        return true;
    }
    // tolerate  {"command": {"command":"dir"}} style
    if (it != obj.MemberEnd() && it->value.IsObject())
        return getString(it->value, key, out);
    return false;
}

} // namespace CppAgent::json
