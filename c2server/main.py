import asyncio

import uvicorn
import uvloop
from darkscryc2server.api.app import app
from darkscryc2server.core.config import settings
from darkscryc2server.core.server import WebSocketServer


async def _run_servers() -> None:
    ws_server = WebSocketServer()
    config = uvicorn.Config(app, host=settings.host, port=settings.port)
    api_server = uvicorn.Server(config)
    app.state.conn_manager = ws_server.conn_manager
    await asyncio.gather(ws_server.start(), api_server.serve())


def main() -> None:
    uvloop.install()
    asyncio.run(_run_servers())


if __name__ == "__main__":
    main()
