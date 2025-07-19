# ======================================================================
# 🌎 Project: DarkScryCpp – Top‑Level CMakeLists.txt
# ======================================================================

cmake_minimum_required(VERSION 3.14)
project(DarkScryCpp VERSION 1.0 LANGUAGES CXX)

# ----------------------------------------------------------------------
# 🔧 Global compiler settings
# ----------------------------------------------------------------------
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

function(enable_compiler_warnings target)
    if (MSVC)
        target_compile_options(${target} PRIVATE /W4 /permissive-)
    else ()
        target_compile_options(${target} PRIVATE -Wall -Wextra -Wpedantic)
    endif ()
endfunction()
function(enable_optimizations target)
    if(MSVC)
        target_compile_options(${target} PRIVATE
            $<$<CONFIG:Release>:/Os /GL>  # /Os optimizes specifically for size
        )
        target_link_options(${target} PRIVATE
            $<$<CONFIG:Release>:/LTCG /OPT:REF /OPT:ICF>
        )
    else()
        target_compile_options(${target} PRIVATE
            $<$<CONFIG:Release>:-Os -ffunction-sections -fdata-sections -flto>
        )
        target_link_options(${target} PRIVATE
            $<$<CONFIG:Release>:-flto -Wl,--gc-sections -s> # "-s" strips debug symbols
        )
    endif()
endfunction()


# ----------------------------------------------------------------------
# 📦 External dependencies (FetchContent)
# ----------------------------------------------------------------------
include(FetchContent)

FetchContent_Declare(
    websocketpp
    GIT_REPOSITORY https://github.com/zaphoyd/websocketpp.git
    GIT_TAG        0.8.2
)
FetchContent_MakeAvailable(websocketpp)
if (UNIX)
    file(READ ${websocketpp_SOURCE_DIR}/websocketpp/logger/basic.hpp WS_BASIC)
    string(REPLACE "~basic<concurrency,names>()" "~basic()" WS_BASIC "${WS_BASIC}")
    string(REPLACE "basic<concurrency,names>(" "basic(" WS_BASIC "${WS_BASIC}")
    string(REPLACE "basic<concurrency,names>" "basic" WS_BASIC "${WS_BASIC}")
    file(WRITE ${websocketpp_SOURCE_DIR}/websocketpp/logger/basic.hpp "${WS_BASIC}")
    file(READ ${websocketpp_SOURCE_DIR}/websocketpp/endpoint.hpp WS_EP)
    string(REPLACE "~endpoint<connection,config>()" "~endpoint()" WS_EP "${WS_EP}")
    file(WRITE ${websocketpp_SOURCE_DIR}/websocketpp/endpoint.hpp "${WS_EP}")
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

# ----------------------------------------------------------------------
# ⚙️  Global compile definitions
# ----------------------------------------------------------------------
add_compile_definitions(ASIO_STANDALONE _WEBSOCKETPP_CPP11_STL_)

# ----------------------------------------------------------------------
# 🧩 Internal modules  (⚠️ order matters!)
# ----------------------------------------------------------------------
add_subdirectory(src/utils/Logger)            # no deps
if(WIN32)
    add_subdirectory(src/utils/win32)         # Win32Utils (needed by Execution)
endif()

add_subdirectory(src/attacks)                 # Attacks / Execution (needs Win32Utils)

add_subdirectory(src/core/CommandHandler)     # CommandHandler (needs Attacks)

add_subdirectory(src/comm/WsClient)           # WsClient (needs CommandHandler)

add_subdirectory(src/mitre)                   # header‑only

add_subdirectory(src/core) 

# ----------------------------------------------------------------------
# 🚀 Main executable
# ----------------------------------------------------------------------
set(APP_SRCS 
    src/main.cpp
)
add_executable(DarkScryCpp ${APP_SRCS})

target_link_libraries(DarkScryCpp PRIVATE
    Core
    Logger
    WsClient
    CommandHandler
    Attacks
    Mitre
    $<$<PLATFORM_ID:Windows>:Win32Utils>
)

target_include_directories(DarkScryCpp PRIVATE
    ${PROJECT_SOURCE_DIR}/src
)

enable_compiler_warnings(DarkScryCpp)
enable_optimizations(DarkScryCpp)