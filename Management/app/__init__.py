from fastapi import FastAPI

from .core.settings import get_settings
from .routers import agents, auth, users


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(debug=settings.debug)
    app.include_router(auth.router, description="Agents management")
    app.include_router(users.router)
    app.include_router(agents.router)
    return app
