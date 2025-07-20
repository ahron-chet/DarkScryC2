#include <gtest/gtest.h>

#ifdef _WIN32
#include "utils/win32/UserUtils.hpp"

TEST(UserUtilsTest, InvalidUserReturnsEmptySid) {
    std::wstring sid = win32::user::get_sid_by_user_name(L"nonexistent_user_1234");
    EXPECT_TRUE(sid.empty());
}
#endif
