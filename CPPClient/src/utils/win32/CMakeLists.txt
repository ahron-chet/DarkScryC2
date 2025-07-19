add_library(Win32Utils STATIC
    Security.cpp
    Process.cpp
    include/Security.hpp
    include/Process.hpp
    include/WinHandle.hpp
)

target_include_directories(Win32Utils PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

target_include_directories(Win32Utils PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}
)

enable_compiler_warnings(Win32Utils)
