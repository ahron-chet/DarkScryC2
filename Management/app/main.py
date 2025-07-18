from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.database import init_db
from .core.settings import get_app_settings
from .routers import agents, auth, modules, tasks, users, ws
from .utils.tasks import close_task_executors

settings = get_app_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_task_executors()


app = FastAPI(title="Management API", debug=settings.debug, lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(agents.router)
app.include_router(tasks.router)
app.include_router(modules.router)
app.include_router(ws.router)


@app.websocket("/ws/simple")
async def simple_websocket(websocket):
    print("✅ Simple handler reached")
    await websocket.accept()
    await websocket.send_text("Hello WebSocket!")
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except:
        print("Client disconnected")