add_library(WsClient STATIC WsClient.cpp WsClient.h)

target_include_directories(WsClient PUBLIC 
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${websocketpp_SOURCE_DIR}
    ${asio_SOURCE_DIR}/asio/include
)

# Ensure definitions explicitly (though root definition should be sufficient)
target_compile_definitions(WsClient PUBLIC ASIO_STANDALONE _WEBSOCKETPP_CPP11_STL_)

enable_compiler_warnings(WsClient)
