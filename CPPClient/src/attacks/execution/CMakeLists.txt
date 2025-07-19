add_library(Execution STATIC
    shell_service/Shell.cpp
    shell_service/Shell.hpp
)

target_include_directories(Execution PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/shell_service
    ${PROJECT_SOURCE_DIR}/src/utils
)

target_link_libraries(Execution PUBLIC Win32Utils)

