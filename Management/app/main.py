from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import tasks
from .core.database import init_db
from .core.settings import get_settings
from .middleware.rate_limit import RateLimitMiddleware
from .routers import agents, auth, users

settings = get_settings()
app = FastAPI(title="Management API", debug=settings.debug)

app.add_middleware(RateLimitMiddleware, max_requests=100, window=60)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup() -> None:
    await init_db()
    await tasks.init_redis()


@app.on_event("shutdown")
async def on_shutdown() -> None:
    await tasks.close_redis()


for router in [auth.router, users.router, agents.router]:
    app.include_router(router)
