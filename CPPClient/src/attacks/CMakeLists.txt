add_library(Attacks INTERFACE)

target_include_directories(Attacks INTERFACE
    ${CMAKE_CURRENT_SOURCE_DIR}
)

if(WIN32)
    add_subdirectory(execution)
    target_link_libraries(Attacks INTERFACE Execution)
endif()
