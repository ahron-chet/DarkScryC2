# DarkScry C2 Server

This directory contains the refactored WebSocket server and management API. It is designed to run independently from the legacy Django backend while providing the same communication features.

## Setup

1. Install the dependencies using [Poetry](https://python-poetry.org/):

```bash
poetry install --no-interaction
```

2. Start the server locally:

```bash
poetry run python main.py
```

Both the management API and the WebSocket listener will start.

## Environment Variables

Configuration is provided entirely through environment variables. The most common settings are:

| Variable | Default | Description |
| -------- | ------- | ----------- |
| `C2_SERVER_HOST` | `0.0.0.0` | Host interface for both the API and WebSocket server |
| `C2_SERVER_PORT` | `9100` | Port for the FastAPI management API |
| `C2_SERVER_WS_PORT` | `876` | Port for agent WebSocket connections |
| `C2_SERVER_REDIS_HOST` | `localhost` | Redis host used for connection tracking |
| `C2_SERVER_REDIS_PASSWORD` | `None` | Redis password if required |
| `C2_SERVER_REDIS_DB` | `0` | Redis database number |
| `C2_SERVER_SSL_CERT` | `None` | Path to an optional TLS certificate |
| `C2_SERVER_SSL_KEY` | `None` | Path to the matching TLS key |

## Usage Examples

### Listing active connections

```bash
curl http://localhost:9100/connections
```

### Sending a command to an agent

```bash
curl -X POST http://localhost:9100/command/<agent_id> \
     -H "Content-Type: application/json" \
     -d '{"command": "echo hi"}'
```

### Manager WebSocket

Connect to `/manager_ws` to interactively query connection state:

```bash
websocat ws://localhost:9100/manager_ws
```

## Testing Guidelines

Before sending a pull request, format and test the code:

```bash
black .
isort .
poetry run pytest -v tests/
```

These commands mirror the instructions in `AGENTS.md` and ensure consistent formatting and reliable tests.
