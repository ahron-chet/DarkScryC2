add_library(CommandHandler STATIC CommandHandler.cpp CommandHandler.h)

target_include_directories(CommandHandler PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${rapidjson_SOURCE_DIR}/include
    ..)

enable_compiler_warnings(CommandHandler)
