import asyncio
import uvicorn
from .settings.config import internalapplogger as logger

from .Server import Server 
from .remote_manager.remote_manager import create_manager_app

import os

if os.name == 'posix':
    def run():
        import uvloop
        # Set uvloop as default event loop policy (Linux only)
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

        asyncio.run(main())
else:
    def run():
        asyncio.run(main())

async def main():
    # 1) Create your main C2 Server
    c2_server = Server()
    await c2_server.connection_manager.wait_until_connected()

    # 2) Start the agent server in an async task
    agent_server_task = asyncio.create_task(c2_server.start())

    # 3) Build the manager FastAPI app + uvicorn server
    manager_app = create_manager_app(c2_server)

    config = uvicorn.Config(
        manager_app, 
        host="0.0.0.0", 
        port=9100,
        log_level="info",
    )
    uvicorn_server = uvicorn.Server(config)

    manager_task = asyncio.create_task(uvicorn_server.serve())

    done, pending = await asyncio.wait(
        [agent_server_task, manager_task],
        return_when=asyncio.FIRST_EXCEPTION
    )

    for task in done:
        exc = task.exception()
        if exc:
            logger.error(f"Task crashed: {exc}")
        for p in pending:
            task.cancel()



# if __name__ == "__main__":
#     run()
