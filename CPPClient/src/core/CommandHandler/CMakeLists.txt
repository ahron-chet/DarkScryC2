add_library(CommandHandler STATIC CommandHandler.cpp CommandHandler.h)

target_include_directories(CommandHandler PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${rapidjson_SOURCE_DIR}/include
    ${PROJECT_SOURCE_DIR}/src/utils
    $<$<PLATFORM_ID:Windows>:${PROJECT_SOURCE_DIR}/src/utils/win32>
    $<$<PLATFORM_ID:Windows>:${PROJECT_SOURCE_DIR}/src/attacks/execution/shell_service>
)

if(WIN32)
    target_link_libraries(CommandHandler PUBLIC Execution)
endif()

enable_compiler_warnings(CommandHandler)
