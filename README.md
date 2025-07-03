# DarkScryC2

**For authorized security simulation only**

DarkScryC2 is a multi-component security simulation platform built specifically for training and research. It replicates typical remote management behaviors so defenders can practice detection and response in a controlled lab environment. This project is not production ready and must never be used for unauthorized or malicious actions.
DarkScryC2 scenarios are built around the MITRE ATT&CK framework to emulate
techniques commonly observed in real-world intrusions.


This repository contains:
- **c2server** – Python based server component providing agent communication channels and a FastAPI manager.
- **django** – Django project used for management APIs and asynchronous workers.
- **frontend** – A Next.js application providing the web interface.
- **client** – Proof-of-concept agent originally written in C#; a cross-platform C++ version is being developed for future releases.
- **dockerfiles** and **docker-compose** files to run the stack.

## Repository structure

```
c2server/    # Python server, FastAPI manager and WebSocket/TCP handling
client/      # legacy C# client source (migration to C++ in progress)
django/      # Django backend project
frontend/    # Next.js frontend
Dockerfiles/ # Additional worker images
```

## Architecture

The framework is split into several cooperating services:

- **Server component (`c2server`)** – the communication hub written in Python. It accepts agent
  connections over legacy TCP or WebSocket and stores their state in Redis. A
  built-in FastAPI application exposes management APIs used by the other
  components.
- **Django backend** – provides REST endpoints and asynchronous task execution
  through `arqworker`. It stores agent metadata in PostgreSQL and relies on the
  server component to execute actions.
- **Next.js frontend** – a React based dashboard that talks to the Django APIs
  for operator interaction.
- **C# client** – a prototype Windows agent implementing the command set used by the server for training scenarios. A replacement client written in C++ is under development.

The framework is designed to work in locked-down networks where only the web
browser can reach the internet. The Windows agent ships with an optional
"double proxy" that pairs with a local browser and tunnels all simulation traffic over
WebSocket connections, blending in with normal browsing activity.

## Simulation capabilities

Agents connecting to the server expose a range of modules that can be triggered
through the REST or WebSocket APIs. Core capabilities include:

- Starting an interactive shell and executing arbitrary commands.
- Downloading or uploading files using base64 transfer.
- Listing directory contents and enumerating running processes.
- Collecting browser credentials (Chrome/Edge) and basic Wi‑Fi information.
- Injecting shellcode into remote processes for in-memory payloads.
- Optional "double proxy" mode that tunnels control traffic through a local
  browser, enabling operation when direct network access is blocked.
- Simulation tasks are mapped to MITRE ATT&CK techniques for realistic scenarios.

All operations are queued by the Django backend which persists task results in
the database while the server component handles the low level transport.


## Running with Docker

The easiest way to run the full stack is with Docker Compose. Copy `.env.example` to `.env` and adjust the environment variables (database credentials, JWT secrets, etc.). Then start the services:

```bash
docker compose up --build
```

This will start:

- `c2server` on ports `1234` (legacy TCP) and `876` (WebSocket) with a FastAPI manager on port `9100`.
- `django` API on port `8000` using PostgreSQL and Redis.
- `frontend` on port `3000`.
- supporting `redis`, `postgres`, and an `arqworker` container.

An alternative compose file `docker-compose.ssl.yml` adds volume mounts for TLS certificates when running the server over HTTPS.

## Development

Python dependencies for the server and Django projects are managed with Poetry. Node dependencies for the frontend are managed with npm. Example commands:

```bash
# install Python deps (inside c2server or django)
poetry install

# run the FastAPI manager with the server
poetry run python c2server/test.py

# run Django migrations and start the development server
cd django
poetry run python DarkScryC2Managment/manage.py migrate
poetry run uvicorn DarkScryC2Managment.asgi:application --reload

# start the frontend
cd frontend
npm install
npm run dev
```

## Environment configuration

The `.env.example` file documents all required environment variables including Redis connection, server component host/port and Django database settings. Copy it to `.env` and adjust the values for your environment.

## Testing

No automated tests are provided. Running `pytest` currently reports that no tests are collected.


## Disclaimer

DarkScryC2 exists solely to help organizations test and improve their security. Operate it only in environments where you have been granted explicit permission. Any use of this project for unauthorized access or malicious activity is strictly forbidden. The authors provide this code for educational and defensive scenarios and disclaim responsibility for misuse.
