# src/core/CommandHandler/CMakeLists.txt
add_library(CommandHandler STATIC CommandHandler.cpp CommandHandler.h)

target_include_directories(CommandHandler PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${rapidjson_SOURCE_DIR}/include
    ${PROJECT_SOURCE_DIR}/src/utils
    ${PROJECT_SOURCE_DIR}/src/Attacks
    ${PROJECT_SOURCE_DIR}/src
)

target_link_libraries(CommandHandler PUBLIC Execution)
target_link_libraries(CommandHandler PUBLIC Collection)
target_link_libraries(CommandHandler PRIVATE Serialization)

