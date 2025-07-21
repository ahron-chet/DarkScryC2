add_library(Win32Utils STATIC
    Security.cpp
    Process.cpp
    RegistryUtils.cpp
    WinUtils.cpp
    UserUtils.cpp
    ProcessLauncher.cpp
)

target_include_directories(Win32Utils
    PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include
    PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}
)

enable_compiler_warnings(Win32Utils)
