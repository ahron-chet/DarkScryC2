if(WIN32)
add_library(Execution STATIC
    shell_service/Shell.cpp
)

target_include_directories(Execution PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/shell_service
    ${PROJECT_SOURCE_DIR}/src/utils/win32
)

target_link_libraries(Execution PUBLIC Win32Utils)

enable_compiler_warnings(Execution)
endif()
