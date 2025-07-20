#include "serialization/JsonUtils.h"
#include <gtest/gtest.h>
#include <rapidjson/document.h>

using CppAgent::json::getBool;
using CppAgent::json::getArray;
using CppAgent::json::getObject;

TEST(JsonUtilsTest, GetBool) {
    rapidjson::Document d;
    d.SetObject();
    d.AddMember("flag", true, d.GetAllocator());

    bool v = false;
    EXPECT_TRUE(getBool(d, "flag", v));
    EXPECT_TRUE(v);

    v = false;
    EXPECT_FALSE(getBool(d, "missing", v));
    EXPECT_FALSE(v);
}

TEST(JsonUtilsTest, GetArray) {
    rapidjson::Document d;
    d.SetObject();
    rapidjson::Value arr(rapidjson::kArrayType);
    arr.PushBack(1, d.GetAllocator());
    d.AddMember("nums", arr, d.GetAllocator());

    const rapidjson::Value* out = nullptr;
    EXPECT_TRUE(getArray(d, "nums", out));
    ASSERT_NE(out, nullptr);
    EXPECT_EQ(out->Size(), 1u);

    out = reinterpret_cast<const rapidjson::Value*>(0x1);
    EXPECT_FALSE(getArray(d, "missing", out));
    EXPECT_EQ(out, reinterpret_cast<const rapidjson::Value*>(0x1));
}

TEST(JsonUtilsTest, GetObject) {
    rapidjson::Document d;
    d.SetObject();
    rapidjson::Value obj(rapidjson::kObjectType);
    obj.AddMember("a", 1, d.GetAllocator());
    d.AddMember("obj", obj, d.GetAllocator());

    const rapidjson::Value* out = nullptr;
    EXPECT_TRUE(getObject(d, "obj", out));
    ASSERT_NE(out, nullptr);
    EXPECT_TRUE(out->HasMember("a"));

    out = reinterpret_cast<const rapidjson::Value*>(0x1);
    EXPECT_FALSE(getObject(d, "missing_obj", out));
    EXPECT_EQ(out, reinterpret_cast<const rapidjson::Value*>(0x1));
}
