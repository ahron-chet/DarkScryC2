include(FetchContent)

FetchContent_Declare(
    websocketpp
    GIT_REPOSITORY https://github.com/zaphoyd/websocketpp.git
    GIT_TAG        0.8.2
)
FetchContent_MakeAvailable(websocketpp)
if(UNIX)
    execute_process(
        COMMAND patch -p1 -N -r - -i ${PROJECT_SOURCE_DIR}/patches/websocketpp-cpp20.patch
        WORKING_DIRECTORY ${websocketpp_SOURCE_DIR}
        RESULT_VARIABLE PATCH_RES
    )
    if(NOT PATCH_RES EQUAL 0)
        message(FATAL_ERROR "Failed to patch websocketpp")
    endif()
endif()

FetchContent_Declare(
    asio
    GIT_REPOSITORY https://github.com/chriskohlhoff/asio.git
    GIT_TAG        asio-1-30-2
)
FetchContent_MakeAvailable(asio)

FetchContent_Declare(
    rapidjson
    GIT_REPOSITORY https://github.com/Tencent/rapidjson.git
    GIT_TAG        v1.1.0
)
set(RAPIDJSON_BUILD_EXAMPLES OFF CACHE BOOL "" FORCE)
set(RAPIDJSON_BUILD_TESTS    OFF CACHE BOOL "" FORCE)
set(RAPIDJSON_BUILD_DOC      OFF CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(rapidjson)

add_compile_definitions(ASIO_STANDALONE _WEBSOCKETPP_CPP11_STL_)
