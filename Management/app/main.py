from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import tasks
from .core.database import init_db
from .core.settings import get_settings
from .middleware.rate_limit import RateLimitMiddleware
from .routers import agents, auth, users

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await tasks.init_redis()
    yield
    await tasks.close_redis()


app = FastAPI(title="Management API", debug=settings.debug, lifespan=lifespan)

app.add_middleware(RateLimitMiddleware, max_requests=100, window=60)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


for router in [auth.router, users.router, agents.router]:
    app.include_router(router)
