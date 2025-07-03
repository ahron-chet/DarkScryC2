# C++ Agent Prototype

This directory contains the work-in-progress native rewrite of the DarkScry agent.
Network communication is implemented using the header-only `websocketpp` library
for asynchronous WebSocket support. A small `Logger` class provides console and
file logging similar to the original C# implementation.

Only the basic connection loop is currently implemented. The rest of the C#
modules will be ported over in future updates.

## Building

The native agent uses CMake and depends on `websocketpp`, Boost and OpenSSL.
On Windows you can generate a Visual Studio solution, while other platforms
may use standard Makefiles:

```bash
cmake -S . -B build
cmake --build build --config Release
```
