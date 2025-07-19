# ======================================================================
# 🌎 Project: DarkScryCpp - Top-Level CMakeLists.txt
# ======================================================================

cmake_minimum_required(VERSION 3.14)
project(DarkScryCpp VERSION 1.0 LANGUAGES CXX)

# ----------------------------------------------------------------------
# 🔧 Global Compiler Settings
# ----------------------------------------------------------------------
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

function(enable_compiler_warnings target)
    if(MSVC)
        target_compile_options(${target} PRIVATE /W4 /permissive-)
    else()
        target_compile_options(${target} PRIVATE -Wall -Wextra -Wpedantic)
    endif()
endfunction()

# ----------------------------------------------------------------------
# 📦 External Dependencies (FetchContent)
# ----------------------------------------------------------------------
include(FetchContent)

# websocketpp (WebSocket Library)
FetchContent_Declare(
    websocketpp
    GIT_REPOSITORY https://github.com/zaphoyd/websocketpp.git
    GIT_TAG 0.8.2
)
FetchContent_MakeAvailable(websocketpp)

# Standalone ASIO (no Boost dependency)
FetchContent_Declare(
    asio
    GIT_REPOSITORY https://github.com/chriskohlhoff/asio.git
    GIT_TAG asio-1-30-2
)
FetchContent_MakeAvailable(asio)

# rapidjson (JSON parsing)
FetchContent_Declare(
    rapidjson
    GIT_REPOSITORY https://github.com/Tencent/rapidjson.git
    GIT_TAG v1.1.0
)
set(RAPIDJSON_BUILD_EXAMPLES OFF CACHE BOOL "" FORCE)
set(RAPIDJSON_BUILD_TESTS OFF CACHE BOOL "" FORCE)
set(RAPIDJSON_BUILD_DOC OFF CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(rapidjson)

# ----------------------------------------------------------------------
# ⚙️ Global Definitions (Avoid Boost explicitly)
# ----------------------------------------------------------------------
add_compile_definitions(ASIO_STANDALONE _WEBSOCKETPP_CPP11_STL_)

# ----------------------------------------------------------------------
# 🧩 Internal Modules
# ----------------------------------------------------------------------
add_subdirectory(src/utils/Logger)
add_subdirectory(src/comm/WsClient)
add_subdirectory(src/core/CommandHandler)
add_subdirectory(src/attacks)
add_subdirectory(src/mitre)
add_subdirectory(src/utils/win32)


# ----------------------------------------------------------------------
# 🚀 Main Executable
# ----------------------------------------------------------------------

set(APP_SRCS src/main.cpp)

add_executable(DarkScryCpp ${APP_SRCS})

target_link_libraries(DarkScryCpp PRIVATE Logger WsClient CommandHandler Attacks Mitre Win32Utils)

target_include_directories(DarkScryCpp PRIVATE
    ${PROJECT_SOURCE_DIR}/src
)


enable_compiler_warnings(DarkScryCpp)

# ----------------------------------------------------------------------
# ✅ Testing (toggle with -DBUILD_TESTING=OFF)
# ----------------------------------------------------------------------
