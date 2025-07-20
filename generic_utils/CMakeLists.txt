# GenericUtils CMake configuration

add_library(GenericUtils INTERFACE)

# Expose the include directory to consumers

target_include_directories(GenericUtils INTERFACE
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>)

