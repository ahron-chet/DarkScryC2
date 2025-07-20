add_library(Attacks INTERFACE)

add_subdirectory(Execution)
add_subdirectory(Collection)

target_link_libraries(Attacks INTERFACE Execution Collection)
