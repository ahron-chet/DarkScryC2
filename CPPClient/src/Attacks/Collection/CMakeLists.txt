if(WIN32)
    add_library(Collection STATIC
        Windows/basic_info.cpp
        Windows/basic_info.hpp
    )

    target_include_directories(Collection PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}
        ${CMAKE_CURRENT_SOURCE_DIR}/Windows
        ${PROJECT_SOURCE_DIR}/src/utils
    )

    target_link_libraries(Collection PUBLIC Win32Utils)

elseif(UNIX)
    add_library(Collection STATIC
        Linux/basic_info.cpp
        Linux/basic_info.hpp
    )

    target_include_directories(Collection PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}
        ${CMAKE_CURRENT_SOURCE_DIR}/Linux
        ${PROJECT_SOURCE_DIR}/src/utils
    )
endif()
