# Management Backend

This directory hosts the **FastAPI** based management API which is gradually replacing the legacy Django backend found in `django/`. The service exposes endpoints for managing users, agents and module execution while delegating low level command handling to the `c2server` component.

## Purpose

* Provide a modern async API for DarkScryC2 operators.
* Maintain feature parity with the old Django application during the migration.
* Serve as a central point for authentication, authorization and background task scheduling.

## Key Components

```
Management
├── app           # FastAPI application package
│   ├── controllers    # Reusable controller classes with business logic
│   ├── core           # Database, settings and security utilities
│   ├── middleware     # (placeholder for future middlewares)
│   ├── models         # SQLAlchemy models mirroring the Django schema
│   ├── routers        # Class‑based route definitions
│   ├── schemas        # Pydantic schemas used by the API
│   ├── services       # Domain services handling CRUD and external calls
│   └── utils          # Helpers for background tasks
├── doc           # Additional documentation
├── migrations    # Alembic migrations
├── scripts       # CLI entry points (invoked via `poetry run manager`)
└── tests         # Pytest suite
```

### Controllers and Services
Controllers aggregate common actions (create, update, delete etc.) and are reused by the routers. Each controller relies on a corresponding service class which encapsulates database operations and any interactions with external systems such as the `c2server` API.

### Routers
Routers expose API endpoints using class‑based views. Authentication is enforced via dependencies defined in `app.core.security`. The main routers include:

* `auth` – login and token refresh operations.
* `users` – CRUD operations for user accounts.
* `agents` – CRUD operations for agent records.
* `modules` – execution and collection module endpoints.

### Models and Schemas
SQLAlchemy models in `app/models` follow the existing Django schema closely. Pydantic schemas in `app/schemas` provide validation and documentation for request and response bodies.

### Background Tasks
Long‑running actions (e.g. requesting data from an agent) are scheduled through [ARQ](https://arq-docs.helpmanual.io/) using Redis. `app.utils.tasks` provides helpers to obtain a task executor and to gracefully close the connection on shutdown. A dedicated worker defined in `arq_worker.py` consumes these jobs. Start it with:

```bash
poetry run arq arq_worker.WorkerSettings
```

## External Interactions

* **`c2server`** – The management backend communicates with the Python server component located in `c2server/` via helper functions like `remote_send_command`. This is how agent modules are triggered or shell commands executed.
* **PostgreSQL** – All persistent data is stored in a PostgreSQL database. Connection details are provided via environment variables (`DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`).
* **Redis** – Used for background job scheduling with ARQ (`MANAGEMENT_REDIS_*` variables).

The environment variables required by the service are documented in `doc/settings.md`.

## Development Notes

1. Install dependencies with `poetry install` inside this directory.
2. Configure environment variables (see `.env.example`).
3. Run the app using `poetry run uvicorn app.main:app --reload`.
4. Apply database migrations with `poetry run alembic upgrade head`.
5. Execute tests using `pytest -v Management/tests/`.

During the migration from Django, maintain parity with the original functionality. Follow the guidelines in `AGENTS.MD` for coding style, async usage and PR requirements.
