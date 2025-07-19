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

# Add custom CMake modules
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
include(ProjectOptions)
include(Dependencies)

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

