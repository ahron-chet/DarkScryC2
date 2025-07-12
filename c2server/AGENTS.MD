
# DarkScry C2 WebSocket Server – Development Guide

This directory (`c2server/`) contains the refactored DarkScry C2 WebSocket server (c2server/) along with its associated FastAPI-based management API. It adheres strictly to modern asynchronous programming patterns.
The current `c2server` functions as an agent communication hub implemented in Python. It manages WebSocket connections from agents and provides a minimal management API via FastAPI. Configuration is handled entirely through environment variables, and Redis is used for tracking active connections.
The objective is to fully reconstruct this module from the ground up, ensuring a clean, maintainable architecture. The design should explicitly keep the Management and C2 server as separate containers, promoting clear boundaries and scalability.

---

## 📁 Project Structure

This layout follows best practices, ensuring clear separation of concerns and maintainability:

```
c2server/
├── docker/                  # Dockerfile for containerization
├── main.py                  # Application entry point
├── darkscryc2server/
│   ├── api/                 # Management API endpoints
│   │   ├── routes.py
│   │   └── websocket.py
│   ├── core/                # Core business logic and components
│   │   ├── config.py        # Pydantic configuration management
│   │   ├── connection.py    # WebSocket and Redis connection handling
│   │   ├── server.py        # WebSocket server core implementation
│   │   └── security.py      # Security and authentication utilities
│   ├── models/              # Pydantic data schemas and validation
│   │   ├── messages.py
│   │   └── schemas.py
│   └── utils/               # Utility modules and common helpers
│       ├── logging.py
│       └── helpers.py
└── tests/                   # Unit and integration tests
    ├── unit/
    └── integration/

```

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
