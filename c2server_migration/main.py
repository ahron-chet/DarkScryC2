import asyncio
import os
import uvicorn

from darkscryc2server.server.websocket_server import WebSocketServer
from darkscryc2server.api.app import app
from darkscryc2server.config.settings import settings


def main() -> None:
    if os.name == "posix":
        import uvloop
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    ws_server = WebSocketServer()

    loop = asyncio.get_event_loop()
    loop.create_task(ws_server.start())
    uvicorn.run(app, host=settings.c2_server_host, port=settings.c2_server_port)


if __name__ == "__main__":
    main()
