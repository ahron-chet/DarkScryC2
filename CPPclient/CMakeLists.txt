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
    GIT_TAG 0.8.2
)
FetchContent_MakeAvailable(websocketpp)

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

    target_link_libraries(unit_tests PRIVATE Logger GTest::gtest_main)

    # Include directories for tests
    target_include_directories(unit_tests PRIVATE ${PROJECT_SOURCE_DIR}/include/DarkScryCpp)

    target_compile_features(unit_tests PUBLIC cxx_std_20)
    enable_compiler_warnings(unit_tests)

    # Register tests with CTest
    include(GoogleTest)
    gtest_discover_tests(unit_tests DISCOVERY_MODE PRE_TEST)
endif()
