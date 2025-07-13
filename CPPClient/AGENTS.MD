# C++ Agent Development Guidelines

This directory contains the standalone C++ agent. The project follows a modular structure to keep core logic, communication, and utilities clearly separated. Each folder has a narrow responsibility so new modules are easy to add and the project scales cleanly.

## Directory Layout

```
/src/
    /core/       # Agent orchestration and command processing
    /comm/       # Communication (WebSocket client etc.)
    /attacks/    # Attack simulation modules
    /mitre/      # MITRE ATT&CK mapping logic
    /utils/      # Utilities, logging, configuration
    main.cpp     # Entry point
/tests/
    /core/
    /attacks/
    /mitre/
/scripts/
    build.cake   # Cake build script
/docs/
CMakeLists.txt
README.md
```

Placeholders for `attacks` and `mitre` libraries are included. Extend these directories with actual implementations as needed.

Use this layout as a guide when adding new components. Keep modules small and focused.
Class names follow PascalCase (e.g., `WsClient`, `CommandHandler`).
Header and source files share the class name to keep includes predictable.
