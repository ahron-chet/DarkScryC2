#pragma once
#include <string>
#include <sstream>
#include <cstdint>

#include <string_view>
#include <algorithm>
#include <cwctype>

namespace utils {

inline std::string bytes_to_gb(std::uint64_t bytes, int precision = 0) {
    double gb = static_cast<double>(bytes) / (1024.0 * 1024.0 * 1024.0);
    std::ostringstream oss;
    oss.setf(std::ios::fixed, std::ios::floatfield);
    oss.precision(precision);
    oss << gb << " GB";
    return oss.str();
}
inline bool iequals(const std::wstring_view lhs, const std::wstring_view rhs) {
    return std::ranges::equal(lhs, rhs, [](wchar_t a, wchar_t b) {
        return std::towlower(a) == std::towlower(b);
    });
}
} // namespace utils
