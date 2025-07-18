if(WIN32)
add_library(Win32Utils STATIC
    WinHandle.hpp
    Security.cpp
    Process.cpp
)

target_include_directories(Win32Utils PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

enable_compiler_warnings(Win32Utils)
endif()
