add_library(Logger STATIC Logger.cpp)

target_include_directories(Logger PUBLIC
    ${PROJECT_SOURCE_DIR}/modules
)
