add_library(WsClient STATIC src/WsClient.cpp)

target_include_directories(WsClient PUBLIC
    ${PROJECT_SOURCE_DIR}/include
)

target_link_libraries(WsClient PRIVATE websocketpp::websocketpp)
