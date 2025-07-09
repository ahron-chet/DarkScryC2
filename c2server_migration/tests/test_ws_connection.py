import asyncio
import os
import sys

import pytest
import websockets

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
os.environ.setdefault("C2_SERVER_HOST", "127.0.0.1")
os.environ.setdefault("C2_SERVER_PORT", "9100")
os.environ.setdefault("C2_SERVER_REDIS_URL", "redis://localhost")

from darkscryc2server.core.connection import WsConnection


@pytest.mark.asyncio
async def test_send_and_receive():
    received = []
    done = asyncio.Event()

    async def handler(websocket):
        conn = WsConnection(websocket=websocket, id="a1")
        resp = await conn.send_and_receive("ping")
        received.append(resp)
        await conn.close()
        done.set()

    server = await websockets.serve(handler, "localhost", 0)
    port = server.sockets[0].getsockname()[1]
    async with server:
        async with websockets.connect(f"ws://localhost:{port}/agent/a1") as ws:
            msg = await ws.recv()
            assert msg == "ping"
            await ws.send("pong")
            await done.wait()

    assert received == ["pong"]
