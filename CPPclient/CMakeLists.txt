# CMakeLists.txt : CMake project for DarkScryCpp
cmake_minimum_required(VERSION 3.8)

# Enable Hot Reload for MSVC compilers if supported.
if (POLICY CMP0141)
    cmake_policy(SET CMP0141 NEW)
    set(CMAKE_MSVC_DEBUG_INFORMATION_FORMAT 
        "$<IF:$<AND:$<C_COMPILER_ID:MSVC>,$<CXX_COMPILER_ID:MSVC>>,$<$<CONFIG:Debug,RelWithDebInfo>:EditAndContinue>,$<$<CONFIG:Debug,RelWithDebInfo>:ProgramDatabase>>"
    )
endif()

project("DarkScryCpp")

# Automatically gather all .cpp source files under src/
file(GLOB_RECURSE SRC_FILES CONFIGURE_DEPENDS "src/*.cpp")

# Define executable with gathered sources (no explicit header inclusion!)
add_executable(DarkScryCpp ${SRC_FILES})

# Set C++ standard explicitly
set_property(TARGET DarkScryCpp PROPERTY CXX_STANDARD 20)

# Explicitly define include directories
target_include_directories(DarkScryCpp PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/include)


add_subdirectory(modules/Logger)

target_link_libraries(DarkScryCpp PRIVATE Logger)

# TODO: Add tests and install targets if needed.
