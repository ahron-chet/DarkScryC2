from fastapi import FastAPI, Depends

from ..config.settings import settings
from ..connections.manager import ConnectionManager
from . import routes
from .ws_manager import manager_ws_endpoint


def get_manager() -> ConnectionManager:
    return ConnectionManager(settings.redis_url)

app = FastAPI(title="C2 Management API")

app.dependency_overrides[ConnectionManager] = get_manager
app.include_router(routes.router)
app.add_api_websocket_route("/manager_ws", manager_ws_endpoint)

@app.get("/health")
async def health():
    return {"status": "ok"}
