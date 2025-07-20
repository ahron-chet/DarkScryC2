# 🚀 DarkScry C++ Agent – Developer & Contributor Guide

Welcome to the **DarkScry C++ Agent** project! This document provides guidelines and best practices for contributing, extending, and maintaining the agent. This is an **actively evolving project**, with new commands, attacks, and features continually being integrated.

Contributors are highly encouraged to expand and enhance the capabilities following these instructions.

---

## 📂 Project Structure (Ongoing)

The project currently follows this organized layout, but it will **expand as new modules and capabilities are added**:

```
CPPClient/
├── src/
│   ├── core/                 # Core agent logic, lifecycle, command handling
│   │   ├── Agent.{h,cpp}
│   │   ├── Config.h
│   │   └── CommandHandler/   # JSON-driven command dispatcher (extensible)
│   │
│   ├── comm/                 # Networking modules, e.g., WebSocket client
│   │   └── WsClient/
│   │
│   ├── Attacks/              # Attack & simulation modules (open for extension)
│   │   ├── Execution/        # Shell interactions, execution modules
│   │   └── Collection/       # System info collection modules
│   │
│   ├── serialization/        # JSON serialization & helpers
│   │
│   ├── mitre/                # MITRE ATT&CK mappings
│   │
│   └── utils/                # Shared utilities, logging, platform-specific code
│       ├── Logger/
│       └── win32/
│
├── tests/                    # Unit tests (actively maintained & growing)
├── scripts/                  # Build scripts (placeholders for now)
├── docs/                     # Documentation (actively evolving)
├── cmake/                    # CMake helpers and configuration scripts
└── main.cpp                  # Entry point (instantiates Agent class)
```

---

## 🛠️ Adding New Commands & Attacks

The **DarkScry Agent** is intentionally structured to easily incorporate new capabilities:

* **To add a new command:**

  * Implement handling logic inside the `CommandHandler`.
  * Add your command ID clearly in the existing command enumeration.
  * Use provided serialization helpers.

* **To add a new attack module:**

  * Create platform-specific implementations under `Attacks/Execution` or `Attacks/Collection`.
  * Ensure the new module integrates cleanly with the existing command-handling workflow.

New attack modules are always welcome. Use the existing structure as a reference point:

```
Attacks/
├── Execution/
│   ├── Windows/      # Windows-specific execution logic
│   └── Linux/        # Linux-specific execution logic
│
└── Collection/
    ├── Windows/      # Windows-specific collection modules
    └── Linux/        # Linux-specific collection modules
```

---

## 📌 Where to Implement Your Features?

Here are some ongoing recommendations when adding new code:

* **Core (`core/`)**:

  * Command parsing, orchestration, and dispatch logic.
  * Extendable command registry allows straightforward integration of future commands.

* **Communication (`comm/`)**:

  * Add networking enhancements here.
  * Ensure communication modules delegate command execution to the `CommandHandler`.

* **Attacks (`Attacks/`)**:

  * Implement new payloads, shell executions, or system information collection.
  * Keep logic isolated for ease of testing and integration.

* **Serialization (`serialization/`)**:

  * JSON serialization utilities and helpers.
  * Extend as needed for complex data structures.

* **Utils (`utils/`)**:

  * Place commonly shared and reusable functionality here (e.g., logging, platform utilities).
  * Encouraged to grow organically as more capabilities are developed.

---

## ✅ Recommended Practices (Always Evolving)

The project adopts these conventions, but **feedback and improvements** are continuously welcome:

| Aspect              | Recommendation                   | Example             |
| ------------------- | -------------------------------- | ------------------- |
| **Classes/Structs** | Use PascalCase                   | `CommandHandler`    |
| **Functions**       | snake\_case                      | `execute_command()` |
| **Variables**       | snake\_case with trailing `_`    | `shell_running_`    |
| **Files**           | Match associated classes/structs | `Shell.{cpp,h}`     |

Always use provided utilities and helpers:

* **Logging**: Utilize global logging utilities (`Logger`).
* **JSON Parsing**: Prefer existing `serialization/JsonUtils.h` helpers.
* **Platform Checks**: Keep platform-specific code clearly separated (`#ifdef _WIN32`, etc.).

---

## 🚦 Ongoing Commands & Extensions

The existing set of commands is just the starting point. The command dispatcher (`CommandHandler`) is designed to seamlessly incorporate future commands:

| ID | Command Name            | Current Purpose (extendable)           |
| -- | ----------------------- | -------------------------------------- |
| 1  | **StartShell**          | Launches an interactive command shell. |
| 2  | **RunCommand**          | Executes shell commands remotely.      |
| 3  | **GetBasicMachineInfo** | Retrieves basic system information.    |
| …  | **YourCommandHere**     | Your future commands here!             |

*This table will expand as the project grows.*

---

## 🧪 Testing and Quality Assurance (Always Ongoing)

Unit tests (`tests/`) should always be expanded with each new feature or module:

* Use GoogleTest framework consistently.
* Keep tests organized according to modules they're testing:

  ```
  tests/
  ├── core/
  ├── Attacks/
  └── comm/
  ```
* Writing tests is encouraged and **expected** for new contributions.

---

## 🚀 Building, Running, and Extending the Project

### Building with CMake:

Use existing CMake presets (`CMakePresets.json`):

* Configure & Build Example:

```bash
cmake -B build
cmake --build build
```

This workflow supports easy iteration and testing, allowing you to focus on continuous improvement.

---

## 📖 Documentation & Communication (Keep Updated)

* **Continuously** document your modules (`README.md` within respective folders).
* Clearly comment your code and interfaces.
* Update this file (**`AGENTS.MD`**) periodically as project structure evolves.

---

## 🌟 The Project Is Never Finished

DarkScry Agent is an **ongoing effort**. Contributors and agents are encouraged to:

* Propose new commands and attacks regularly.
* Improve existing modules.
* Suggest structural improvements or new coding practices.

Your contributions shape the project’s direction and success.


