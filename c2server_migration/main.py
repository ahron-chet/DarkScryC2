import asyncio

import uvicorn
import uvloop

from darkscryc2server.api.app import app
from darkscryc2server.core.config import settings
from darkscryc2server.core.server import WebSocketServer


def main() -> None:

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    ws_server = WebSocketServer()

    loop = asyncio.get_event_loop()
    loop.create_task(ws_server.start())
    uvicorn.run(app, host=settings.host, port=settings.port)


if __name__ == "__main__":
    main()
