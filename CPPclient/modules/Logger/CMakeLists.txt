add_library(Logger STATIC src/Logger.cpp)

target_include_directories(Logger PUBLIC
    ${PROJECT_SOURCE_DIR}/include
)
