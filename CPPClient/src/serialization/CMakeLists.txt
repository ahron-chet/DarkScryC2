add_library(Serialization INTERFACE)

# Only headers; set include directory
target_include_directories(Serialization INTERFACE ${PROJECT_SOURCE_DIR}/src/serialization)
