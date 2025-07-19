function(enable_compiler_warnings target)
    if (MSVC)
        target_compile_options(${target} PRIVATE /W4 /permissive-)
    else ()
        target_compile_options(${target} PRIVATE -Wall -Wextra -Wpedantic)
    endif ()
endfunction()

function(enable_optimizations target)
    if(MSVC)
        target_compile_options(${target} PRIVATE
            $<$<CONFIG:Release>:/Os /GL>
        )
        target_link_options(${target} PRIVATE
            $<$<CONFIG:Release>:/LTCG /OPT:REF /OPT:ICF>
        )
    else()
        target_compile_options(${target} PRIVATE
            $<$<CONFIG:Release>:-Os -ffunction-sections -fdata-sections -flto>
        )
        target_link_options(${target} PRIVATE
            $<$<CONFIG:Release>:-flto -Wl,--gc-sections -s>
        )
    endif()
endfunction()
