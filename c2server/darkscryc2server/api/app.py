from fastapi import Depends, FastAPI

from ..core.config import settings
from ..core.connection import ConnectionManager
from ..utils.logging import setup_logging
from . import routes
from .websocket import manager_ws_endpoint


def get_manager() -> ConnectionManager:
    return ConnectionManager(settings.redis_url)


setup_logging()
app = FastAPI(title="C2 Management API")

app.dependency_overrides[ConnectionManager] = get_manager
app.include_router(routes.router)
app.add_api_websocket_route("/manager_ws", manager_ws_endpoint)


@app.get("/health")
async def health():
    return {"status": "ok"}
