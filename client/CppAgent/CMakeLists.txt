cmake_minimum_required(VERSION 3.16)
project(CppAgent LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include(FetchContent)
FetchContent_Declare(
    websocketpp
    GIT_REPOSITORY https://github.com/zaphoyd/websocketpp.git
    GIT_TAG        0.8.2
)
FetchContent_MakeAvailable(websocketpp)

find_package(Boost REQUIRED COMPONENTS system thread)
find_package(OpenSSL REQUIRED)

add_executable(CppAgent
    main.cpp
    Logger.cpp
    NetworkClient.cpp
)

target_include_directories(CppAgent PRIVATE ${websocketpp_SOURCE_DIR})

target_link_libraries(CppAgent PRIVATE Boost::system Boost::thread OpenSSL::SSL)

