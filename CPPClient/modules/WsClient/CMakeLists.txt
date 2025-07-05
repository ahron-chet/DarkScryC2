add_library(WsClient STATIC WsClient.cpp)

target_include_directories(WsClient PUBLIC
    ${PROJECT_SOURCE_DIR}/modules
    ${websocketpp_SOURCE_DIR}
    ${asio_SOURCE_DIR}/asio/include
)

target_compile_definitions(WsClient PUBLIC ASIO_STANDALONE)

enable_compiler_warnings(WsClient)
