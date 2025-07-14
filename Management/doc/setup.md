# Management Backend Setup

This document describes how to set up the FastAPI Management backend.

1. Ensure Python 3.10+ and [Poetry](https://python-poetry.org/) are installed.
2. Install dependencies:
   ```bash
   poetry install
   ```
3. Configure environment variables as described in `.env.example`.
4. Run the application:
   ```bash
   poetry run uvicorn app.main:app --reload
   ```
5. Run database migrations:
   ```bash
   poetry run alembic upgrade head
   ```
6. Start the background task worker:
   ```bash
   poetry run arq arq_worker.WorkerSettings
   ```

Tests can be executed with:
```bash
pytest -v Management/tests/
```
