add_library(Core STATIC
    Agent.cpp
    Agent.h
)

target_include_directories(Core PUBLIC
    ${PROJECT_SOURCE_DIR}/src         # for "Config.h", etc.
)

target_link_libraries(Core PUBLIC
    Logger
    WsClient
)
