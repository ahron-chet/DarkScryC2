set(include
    include/WinHandle.hpp
    include/Security.hpp
    include/Process.hpp
)

set(SOURCES
    Security.cpp
    Process.cpp
)

add_library(Win32Utils STATIC ${include} ${SOURCES})

# Allow public includes like: "utils/win32/WinHandle.hpp"
target_include_directories(Win32Utils PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

# Still let .cpps include their siblings directly
target_include_directories(Win32Utils PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}
)

enable_compiler_warnings(Win32Utils)
