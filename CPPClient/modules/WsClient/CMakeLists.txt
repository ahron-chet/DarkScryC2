add_library(WsClient STATIC WsClient.cpp WsClient.h)

target_include_directories(WsClient PUBLIC 
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${websocketpp_SOURCE_DIR}
    ${asio_SOURCE_DIR}/asio/include
    ${CMAKE_SOURCE_DIR}/modules/Logger   # <-- explicitly added
)

# Explicitly reinforce standalone definitions
target_compile_definitions(WsClient PUBLIC ASIO_STANDALONE _WEBSOCKETPP_CPP11_STL_)


enable_compiler_warnings(WsClient)
