add_library(Attacks INTERFACE)

add_subdirectory(execution)
add_subdirectory(collection)

target_link_libraries(Attacks INTERFACE Execution Collection)
