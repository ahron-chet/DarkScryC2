# DarkScry C2 Server Migration

This directory contains the refactored `c2server` implementation. The goal is to provide a clean architecture with a WebSocket server for agents and a management API exposed via FastAPI. Configuration is handled through Pydantic settings and environment variables. Redis stores connection metadata so multiple processes can access active agent information.

## Project Layout
```
c2server_migration/
├── docker/
│   └── Dockerfile
├── pyproject.toml
├── README.md
├── main.py
└── darkscryc2server/
    ├── config/
    ├── server/
    ├── api/
    ├── connections/
    ├── models/
    └── utils/
```

Run the server using `python main.py`. On POSIX systems `uvloop` is enabled
automatically for better performance:
```bash
python main.py
```

### Management WebSocket

The management API exposes `/manager_ws` for interactive control. Example usage
with `websockets`:

```python
import asyncio
import websockets
import json

async def main():
    async with websockets.connect("ws://localhost:9100/manager_ws") as ws:
        await ws.send(json.dumps({"action": "get_connections"}))
        print(await ws.recv())

asyncio.run(main())
```

Commands sent via `/command/{agent_id}` and the WebSocket interface expect a
response from the agent using the `send_and_receive` helper on `WsConnection`.
