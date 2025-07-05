# ======================================================================
#  Top-level CMakeLists.txt  – DarkScryCpp
# ======================================================================

cmake_minimum_required(VERSION 3.14)            # FetchContent ≥ 3.14
project(DarkScryCpp VERSION 1.0 LANGUAGES CXX)

# ----------------------------------------------------------------------
# 1. Global compiler settings
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
# 2. Logger library  (modules/Logger)  – LEAVE ITS OWN CMake AS-IS
# ----------------------------------------------------------------------
add_subdirectory(modules/Logger)      # creates target: Logger

# ----------------------------------------------------------------------
# 2b. Fetch websocketpp library for WebSocket networking
# ----------------------------------------------------------------------
include(FetchContent)
FetchContent_Declare(
    websocketpp
    GIT_REPOSITORY https://github.com/zaphoyd/websocketpp.git
    GIT_TAG 0.8.2
)
FetchContent_MakeAvailable(websocketpp)


# ----------------------------------------------------------------------
# 3. Main executable
# ----------------------------------------------------------------------
file(GLOB_RECURSE APP_SRCS CONFIGURE_DEPENDS src/*.cpp)

add_subdirectory(modules/WsClient)

add_executable(DarkScryCpp ${APP_SRCS})
target_link_libraries(DarkScryCpp PRIVATE Logger WsClient)



# ----------------------------------------------------------------------
# 4. Unit-tests  (toggle with -DBUILD_TESTING=OFF)
# ----------------------------------------------------------------------
include(CTest)                                # defines BUILD_TESTING
if (BUILD_TESTING)
    # ---- 4a.  GoogleTest ----------------------------------------------------
    include(FetchContent)
    FetchContent_Declare(
        googletest
        URL https://github.com/google/googletest/archive/refs/tags/v1.14.0.zip
    )
    set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)     # MSVC runtime
    FetchContent_MakeAvailable(googletest)                 # GTest::gtest_main

    # ---- 4b.  Build a single test binary -----------------------------------
    file(GLOB TEST_SRCS CONFIGURE_DEPENDS tests/*.cpp)
    add_executable(unit_tests ${TEST_SRCS})
    target_link_libraries(unit_tests PRIVATE Logger GTest::gtest_main)

    # same extra include dir for the tests
    target_include_directories(unit_tests
        PRIVATE ${PROJECT_SOURCE_DIR}/include/DarkScryCpp
    )
    target_compile_features(unit_tests PUBLIC cxx_std_20)
    enable_compiler_warnings(unit_tests)

    # ---- 4c.  Register tests with CTest -------------------------------------
    include(GoogleTest)
    gtest_discover_tests(unit_tests DISCOVERY_MODE PRE_TEST)
endif()
