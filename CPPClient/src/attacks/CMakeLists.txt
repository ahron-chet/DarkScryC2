add_library(Attacks INTERFACE)
add_subdirectory(execution)
target_link_libraries(Attacks INTERFACE Execution)
