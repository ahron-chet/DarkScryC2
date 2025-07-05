# ======================================================================
# 🌎 Project: DarkScryCpp - Top-Level CMakeLists.txt
# ======================================================================

cmake_minimum_required(VERSION 3.14)
project(DarkScryCpp VERSION 1.0 LANGUAGES CXX)

# ----------------------------------------------------------------------
# 🔧 Global Compiler Settings
# ----------------------------------------------------------------------
set(CMAKE_CXX_STANDARD 17)
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

# ----------------------------------------------------------------------
# ⚙️ Global Definitions (Avoid Boost explicitly)
# ----------------------------------------------------------------------
add_compile_definitions(ASIO_STANDALONE _WEBSOCKETPP_CPP11_STL_)

# ----------------------------------------------------------------------
# 🧩 Internal Modules
# ----------------------------------------------------------------------
add_subdirectory(modules/Logger)
add_subdirectory(modules/WsClient)

# ----------------------------------------------------------------------
# 🚀 Main Executable
# ----------------------------------------------------------------------
file(GLOB_RECURSE APP_SRCS CONFIGURE_DEPENDS src/*.cpp src/*.h)

add_executable(DarkScryCpp ${APP_SRCS})

target_link_libraries(DarkScryCpp PRIVATE Logger WsClient)

target_include_directories(DarkScryCpp PRIVATE
    ${PROJECT_SOURCE_DIR}/src
    ${PROJECT_SOURCE_DIR}/modules
)

enable_compiler_warnings(DarkScryCpp)

# ----------------------------------------------------------------------
# ✅ Testing (toggle with -DBUILD_TESTING=OFF)
# ----------------------------------------------------------------------
include(CTest)
if(BUILD_TESTING)
    FetchContent_Declare(
        googletest
        URL https://github.com/google/googletest/archive/refs/tags/v1.14.0.zip
    )
    set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
    FetchContent_MakeAvailable(googletest)

    file(GLOB TEST_SRCS CONFIGURE_DEPENDS tests/*.cpp)

    add_executable(unit_tests ${TEST_SRCS})

    target_link_libraries(unit_tests PRIVATE Logger WsClient GTest::gtest_main)
    target_include_directories(unit_tests PRIVATE
        ${PROJECT_SOURCE_DIR}/src
        ${PROJECT_SOURCE_DIR}/modules
    )

    target_compile_features(unit_tests PUBLIC cxx_std_17)
    enable_compiler_warnings(unit_tests)

    include(GoogleTest)
    gtest_discover_tests(unit_tests DISCOVERY_MODE PRE_TEST)
endif()
