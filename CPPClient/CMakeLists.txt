# ======================================================================
#  Top-level CMakeLists.txt  – DarkScryCpp
# ======================================================================

cmake_minimum_required(VERSION 3.14)  # Required for FetchContent
project(DarkScryCpp VERSION 1.0 LANGUAGES CXX)

# ----------------------------------------------------------------------
# 🌎 Global Compiler Settings
# ----------------------------------------------------------------------
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

function(enable_compiler_warnings tgt)
    if (MSVC)
        target_compile_options(${tgt} PRIVATE /W4 /permissive-)
    else()
        target_compile_options(${tgt} PRIVATE -Wall -Wextra -Wpedantic)
    endif()
endfunction()

# ----------------------------------------------------------------------
# 📦 External Dependencies (FetchContent)
# ----------------------------------------------------------------------
include(FetchContent)

# websocketpp (Header-only WebSocket Library)
FetchContent_Declare(
    websocketpp
    GIT_REPOSITORY https://github.com/zaphoyd/websocketpp.git
    GIT_TAG 4dfe1be74e684acca19ac1cf96cce0df9eac2a2d
)
FetchContent_MakeAvailable(websocketpp)

# Patch websocketpp for C++20 compatibility
file(READ ${websocketpp_SOURCE_DIR}/websocketpp/logger/basic.hpp WSPP_BASIC)
string(REPLACE "basic<concurrency,names>" "basic" WSPP_BASIC "${WSPP_BASIC}")
file(WRITE ${websocketpp_SOURCE_DIR}/websocketpp/logger/basic.hpp "${WSPP_BASIC}")

file(READ ${websocketpp_SOURCE_DIR}/websocketpp/endpoint.hpp WSPP_EP)
string(REPLACE "~endpoint<connection,config>()" "~endpoint()" WSPP_EP "${WSPP_EP}")
file(WRITE ${websocketpp_SOURCE_DIR}/websocketpp/endpoint.hpp "${WSPP_EP}")

file(READ ${websocketpp_SOURCE_DIR}/websocketpp/roles/server_endpoint.hpp WSPP_SE)
string(REPLACE "server<config>(" "server(" WSPP_SE "${WSPP_SE}")
string(REPLACE "server<config> &" "server &" WSPP_SE "${WSPP_SE}")
string(REPLACE "server<config> &&" "server &&" WSPP_SE "${WSPP_SE}")
string(REPLACE "~server<config>()" "~server()" WSPP_SE "${WSPP_SE}")
file(WRITE ${websocketpp_SOURCE_DIR}/websocketpp/roles/server_endpoint.hpp "${WSPP_SE}")

# asio (Standalone ASIO for websocketpp)
FetchContent_Declare(
    asio
    GIT_REPOSITORY https://github.com/chriskohlhoff/asio.git
    GIT_TAG asio-1-30-2
)
FetchContent_MakeAvailable(asio)

# ----------------------------------------------------------------------
# 🧩 Project Libraries (Modules)
# ----------------------------------------------------------------------
add_subdirectory(modules/Logger)   # Target: Logger
add_subdirectory(modules/WsClient) # Target: WsClient (depends on websocketpp)

# ----------------------------------------------------------------------
# 🚀 Main Executable
# ----------------------------------------------------------------------
# Collect source files automatically
file(GLOB_RECURSE APP_SRCS CONFIGURE_DEPENDS src/*.cpp)

add_executable(DarkScryCpp ${APP_SRCS})

# Link libraries
target_link_libraries(DarkScryCpp PRIVATE Logger WsClient)

# Include directory for agent sources
target_include_directories(DarkScryCpp PRIVATE ${PROJECT_SOURCE_DIR}/src)

# Compiler warnings for executable
enable_compiler_warnings(DarkScryCpp)

# ----------------------------------------------------------------------
# ✅ Testing Setup (toggle with -DBUILD_TESTING=OFF)
# ----------------------------------------------------------------------
include(CTest)
if(BUILD_TESTING)
    # GoogleTest Framework
    FetchContent_Declare(
        googletest
        URL https://github.com/google/googletest/archive/refs/tags/v1.14.0.zip
    )
    set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
    FetchContent_MakeAvailable(googletest)

    # Test executable
    file(GLOB TEST_SRCS CONFIGURE_DEPENDS tests/*.cpp)
    add_executable(unit_tests ${TEST_SRCS})

    target_link_libraries(unit_tests PRIVATE Logger WsClient GTest::gtest_main)

    # Include directories for tests
    target_include_directories(unit_tests PRIVATE ${PROJECT_SOURCE_DIR}/src)

    target_compile_features(unit_tests PUBLIC cxx_std_20)
    enable_compiler_warnings(unit_tests)

    # Register tests with CTest
    include(GoogleTest)
    gtest_discover_tests(unit_tests DISCOVERY_MODE PRE_TEST)
endif()
