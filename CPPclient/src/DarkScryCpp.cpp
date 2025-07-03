#include "Logger/Logger.h"
#include <iostream>

using namespace std;

int main()
{
    // Initialize logger (console output enabled)
    CppAgent::Logger logger(true, true, "test.log");

    logger.log("This is an info message.", CppAgent::Logger::Level::Info);
    logger.log("This is a debug message.", CppAgent::Logger::Level::Debug);
    logger.log("This is a warning!", CppAgent::Logger::Level::Warning);
    logger.log("This is an error!", CppAgent::Logger::Level::Error);
    logger.log("This is a critical error!", CppAgent::Logger::Level::Critical);

    cout << "Logger test completed." << endl;
    return 0;
}
