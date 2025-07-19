if(WIN32)
    add_library(Collection STATIC
        system_information/windows_basic_info.cpp
        system_information/windows_basic_info.hpp
    )

    target_include_directories(Collection PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/system_information
        ${PROJECT_SOURCE_DIR}/src/utils
    )

    target_link_libraries(Collection PUBLIC Win32Utils)

elseif(UNIX)
    add_library(Collection STATIC
        system_information/linux_basic_info.cpp
        system_information/linux_basic_info.hpp
    )

    target_include_directories(Collection PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/system_information
    )
endif()
