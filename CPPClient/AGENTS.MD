Here's a clearer, structured **`AGENTS.MD`** to guide developers effectively when working with your existing project layout:

---

# 🚀 DarkScry C++ Agent Development Guidelines

This document explains the project layout, coding conventions, and best practices for contributing or extending the **DarkScry C++ Agent**. Follow these guidelines closely to ensure code consistency, ease of maintenance, and smooth integration.

---

## 📂 Project Directory Layout

The project is structured into clearly defined modules, each with specific responsibilities:

```
src/
├── core/               # Core agent orchestration, lifecycle management, and command handling
│   ├── Agent.cpp
│   ├── Agent.h
│   └── CommandHandler/ # JSON command parsing, task execution, interfaces with attack modules
│
├── comm/               # Communication protocols, WebSocket client implementations
│   └── WsClient/
│
├── attacks/            # Attack simulation modules
│   ├── execution/      # Shell execution & interactive sessions (Windows/Linux specific)
│   └── collection/     # System information & data gathering modules (Windows/Linux specific)
│
├── mitre/              # Mapping functionalities to MITRE ATT&CK framework techniques
│
├── utils/              # Common utilities, logging, configuration management, platform-specific helpers
│   ├── Logger/         # Global logging utilities
│   └── win32/          # Windows-specific helpers (process handling, security utilities)
│
└── main.cpp            # Agent entry point (instantiate and run core agent)
```

---

## 🛠️ How to Choose Where to Place Your Code

Follow this guide when adding new functionality:

### 🟢 **Core (`src/core/`)**

* **Agent orchestration**, startup, shutdown, and general lifecycle management.
* **Command parsing and task handling**: interpreting JSON commands and invoking attack or utility modules.

  Example classes:

  * `Agent`, `CommandHandler`

### 📡 **Communication (`src/comm/`)**

* Network communication logic, WebSocket interactions, server-client protocols.

  Example classes:

  * `WsClient`

### ⚔️ **Attacks (`src/attacks/`)**

* **`execution/`**: Modules for executing commands or scripts, shell interactions (e.g., interactive shells, remote command execution).
* **`collection/`**: Modules for gathering system information, files, processes, users, and more.

  Example files/classes:

  * `Shell`, `windows_basic_info`

  > Attack modules should have no direct knowledge of networking or command handling. Instead, they are invoked by `CommandHandler`.

### 📊 **MITRE (`src/mitre/`)**

* Logic specifically related to mapping agent capabilities to the MITRE ATT\&CK techniques and sub-techniques.

  Example classes:

  * `MitreMapper`

### 🔧 **Utils (`src/utils/`)**

* General-purpose **helper functions**, logging utilities.
* Platform-specific utilities (**Windows-specific utilities go into `win32` subdirectory**).

  Example classes:

  * `Logger`, `Config`, `Security`, `Process`, `WinHandle`

---

## 📜 General Coding Conventions

* **File naming**: Match the class name (e.g., `CommandHandler.hpp` and `CommandHandler.cpp`).
* **Class naming**: Use PascalCase (e.g., `WsClient`, `Agent`, `WinHandle`).
* **Function naming**: Use snake\_case (e.g., `run_command`, `load_config`).
* **Include paths**: Clearly reflect the module's directory structure for predictability (e.g., `#include "utils/Logger/Logger.h"`).
* **General utilities** (like parsing or conversions) must go to `utils` and should be reusable across the project.
* **Module interaction**:

  * `CommandHandler` calls → `attacks` modules (e.g., `Shell`)
  * `Attacks` modules call → `utils` (for helpers/logging)
  * `comm` calls → `core` (`CommandHandler`) to handle incoming commands

---

## 🚦 Recommended Workflow

1. Identify clearly where new functionality belongs (core logic, communication, attack, utility, or MITRE mapping).
2. Follow the directory and class layout conventions strictly.
3. Implement logic within isolated classes to ensure easy unit testing.
4. Ensure all modules are loosely coupled, interacting primarily via clearly defined interfaces.
5. Ensure code modularity when creating new capabilites if you think somthing should go to utils place it in their 

---
**⚠️ Important:**

* Always ensure **modularity** when developing new capabilities.
* If you're implementing common or reusable logic, **place it directly in the `utils/` module**.
* **`CommandHandler`** should **only call** modules inside the **`attacks/`** directory.
* Attack modules (`attacks/`) may freely use utilities from the **`utils/`** directory.

**Happy coding! 🐱‍💻**
