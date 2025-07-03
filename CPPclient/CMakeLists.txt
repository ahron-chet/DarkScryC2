# CMakeLists.txt : CMake project for DarkScryCpp
cmake_minimum_required(VERSION 3.8)

# Enable Hot Reload for MSVC compilers if supported.
if (POLICY CMP0141)
    cmake_policy(SET CMP0141 NEW)
    set(CMAKE_MSVC_DEBUG_INFORMATION_FORMAT 
        "$<IF:$<AND:$<C_COMPILER_ID:MSVC>,$<CXX_COMPILER_ID:MSVC>>,$<$<CONFIG:Debug,RelWithDebInfo>:EditAndContinue>,$<$<CONFIG:Debug,RelWithDebInfo>:ProgramDatabase>>"
    )
endif()

project("DarkScryCpp")

add_subdirectory(modules/Logger)

find_package(GTest REQUIRED)

add_executable(logger_test tests/test_logger.cpp)
set_property(TARGET logger_test PROPERTY CXX_STANDARD 20)
target_include_directories(logger_test PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/include)
target_link_libraries(logger_test PRIVATE Logger GTest::gtest_main)

enable_testing()
add_test(NAME logger_test COMMAND logger_test)

# TODO: Add install targets if needed.
