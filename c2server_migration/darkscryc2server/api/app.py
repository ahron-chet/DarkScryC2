from fastapi import FastAPI, Request, WebSocket

from ..core.config import settings
from ..core.connection import ConnectionManager
from ..utils.logging import setup_logging
from . import routes
from .websocket import manager_ws_endpoint


def get_manager() -> ConnectionManager:
    return ConnectionManager(settings.redis_url)


setup_logging()
app = FastAPI(title="C2 Management API")
app.state.conn_manager = get_manager()
app.include_router(routes.router)


async def _ws_proxy(websocket: WebSocket) -> None:
    class _WSRequest:
        def __init__(self, ws: WebSocket) -> None:
            self.app = ws.app

    await manager_ws_endpoint(websocket, _WSRequest(websocket))


app.add_api_websocket_route("/manager_ws", _ws_proxy)


@app.get("/health")
async def health():
    return {"status": "ok"}
