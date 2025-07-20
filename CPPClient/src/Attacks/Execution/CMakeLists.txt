add_library(Execution STATIC)

if(WIN32)
    target_sources(Execution PRIVATE
        Windows/Shell.cpp
        Windows/Shell.hpp
    )

    target_include_directories(Execution PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}
        ${CMAKE_CURRENT_SOURCE_DIR}/Windows
        ${PROJECT_SOURCE_DIR}/src/utils
    )

    target_link_libraries(Execution PUBLIC Win32Utils)

elseif(UNIX)
    target_sources(Execution PRIVATE
        Linux/Shell.cpp
        Linux/Shell.hpp
    )

    target_include_directories(Execution PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}
        ${CMAKE_CURRENT_SOURCE_DIR}/Linux
        ${PROJECT_SOURCE_DIR}/src/utils
    )
endif()
