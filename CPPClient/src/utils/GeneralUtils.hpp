#pragma once
#include <string>
#include <sstream>
#include <cstdint>

namespace utils {

inline std::string bytes_to_gb(std::uint64_t bytes, int precision = 0) {
    double gb = static_cast<double>(bytes) / (1024.0 * 1024.0 * 1024.0);
    std::ostringstream oss;
    oss.setf(std::ios::fixed, std::ios::floatfield);
    oss.precision(precision);
    oss << gb << " GB";
    return oss.str();
}

} // namespace utils
