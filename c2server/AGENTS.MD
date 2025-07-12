
# DarkScry C2 WebSocket Server – Development Guide

This directory (`c2server/`) contains the refactored DarkScry C2 WebSocket server (c2server/) along with its associated FastAPI-based management API. It adheres strictly to modern asynchronous programming patterns.
The current `c2server` functions as an agent communication hub implemented in Python. It manages WebSocket connections from agents and provides a minimal management API via FastAPI. Configuration is handled entirely through environment variables, and Redis is used for tracking active connections.
The objective is to fully reconstruct this module from the ground up, ensuring a clean, maintainable architecture. The design should explicitly keep the Management and C2 server as separate containers, promoting clear boundaries and scalability.

---

## 📁 Project Structure

Here's a clear and concise way to communicate your idea:

---

This project structure serves as an example of best practices for clear separation of concerns, maintainability, and scalability. Developers should follow these principles, using the provided layout as guidance. Feel free to extend existing directories or create new ones as needed, always aligning with the overall best practices and the conceptual structure shown here.

**Recommended Directory Structure (directories only):**

```
c2server/
├── docker/                  # Docker containerization files
├── darkscryc2server/        # Core application package
│   ├── api/                 # API endpoints and routing
│   ├── core/                # Core business logic components
│   ├── models/              # Data models and schema definitions
│   └── utils/               # Utility functions and common helpers
└── tests/                   # Testing suites
    ├── unit/                # Unit tests
    └── integration/         # Integration tests
```

**Guidelines:**

* Maintain clear separation between layers (API, core logic, models, utilities).
* Add or extend directories based on specific feature needs, ensuring new additions align conceptually with existing best practices.
* Always prioritize readability, maintainability, and modularity.


**Separation of concerns:**

* `server/`: WebSocket handling only.
* `api/`: Management endpoints.
* `connections/`: Connection state management with Redis.
* `models/`: Shared schemas and data validation.
* `utils/`: Helper functions.

---

## 📐 Coding Standards

* Use Python **3.11+** (specified in `pyproject.toml`).
* Code asynchronously (`async def`, `await`) throughout the application.
* Configuration management with `pydantic-settings` using environment variables.
* Use structured logging (`logging` module with JSON format).
* Keep external dependencies minimal and justified.

---

## 🧪 Testing Guidelines

* Write unit tests for critical logic and business rules.
* Integration tests should cover WebSocket interactions and Redis integration.
* Mock external services (Redis/WebSockets) clearly and explicitly.
* Ensure that new functionalities have corresponding test cases.
* Never ignore test warnings. Always resolve them before submitting your PR. If a warning genuinely cannot be fixed, clearly document the reason in your PR description.

Run tests clearly and consistently with:

```bash
pytest -v tests/
```

---

## 🧹 Code Formatting Standards

Before committing, run:

```bash
black .
isort .
```

Consistent formatting helps ensure clarity and maintainability.

---
