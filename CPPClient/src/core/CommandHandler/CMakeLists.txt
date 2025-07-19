add_library(CommandHandler STATIC CommandHandler.cpp CommandHandler.h)

target_include_directories(CommandHandler PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${rapidjson_SOURCE_DIR}/include
    ${PROJECT_SOURCE_DIR}/src/utils
    ${PROJECT_SOURCE_DIR}/src/attacks
)

target_include_directories(CommandHandler PRIVATE "${CMAKE_SOURCE_DIR}/src/attacks")

enable_compiler_warnings(CommandHandler)
