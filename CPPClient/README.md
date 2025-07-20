# DarkScry C++ Agent

This directory contains the experimental C++ client for the DarkScry project. The layout keeps source code, tests, and build scripts organized for clarity. The `core` folder hosts the main `Agent` class and command handling while `comm` contains networking helpers like the WebSocket client.

```
/src
    /core            # Core agent logic
    /comm            # Communication modules
    /Attacks         # Attack simulation modules
    /mitre           # MITRE ATT&CK mappings
    /utils           # Logging, configuration, helpers
    main.cpp         # Entry point
/tests
    /core
    /Attacks
    /mitre
/scripts
    build.cake
/docs
CMakeLists.txt
```

Build with CMake as usual. The `scripts` folder contains a placeholder Cake build script should you prefer that workflow.

The entry point simply instantiates the `Agent` class located in `src/core` and
invokes `run()`. Extend the `Agent` implementation to add new capabilities as
modules under `Attacks` or `mitre`.
