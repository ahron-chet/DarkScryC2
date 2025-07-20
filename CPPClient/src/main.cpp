#define NOMINMAX
#include "Agent.h"

int main() {
    
    CppAgent::Agent agent;
    bool ok = agent.run();
    return ok ? 0 : 1;
}
