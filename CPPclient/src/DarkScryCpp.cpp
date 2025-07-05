
#include <iostream>
#include "Logger.h"
#include "DarkScryCpp/Config.h"

using namespace std;

int main()
{
	CppAgent::Config config;
    CppAgent::Logger logger(true, true, config.LOG_FILE);

    logger.log(std::string(config.AGENT_NAME) + " started", CppAgent::Logger::Level::Info);

    return 0;
}