from fastapi import FastAPI

from .core.settings import get_settings
from .routers import auth, users


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(debug=settings.debug)
    app.include_router(auth.router)
    app.include_router(users.router)
    return app
