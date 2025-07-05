add_library(WsClient STATIC src/WsClient.cpp)

target_include_directories(WsClient PUBLIC
    ${PROJECT_SOURCE_DIR}/include
    ${websocketpp_SOURCE_DIR}
    ${asio_SOURCE_DIR}/asio/include
)

target_compile_definitions(WsClient PRIVATE ASIO_STANDALONE)

enable_compiler_warnings(WsClient)
