add_library(Logger STATIC Logger.cpp Logger.h GlobalLogger.h)

target_include_directories(Logger PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

