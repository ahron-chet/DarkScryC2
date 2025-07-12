import asyncio

import pytest
from darkscryc2server.core.connection import ConnectionManager, WsConnection


class DummyWebSocket:
    def __init__(self) -> None:
        self.remote_address = ("127.0.0.1", 0)
        self.closed = False

    async def close(self) -> None:
        self.closed = True


@pytest.mark.asyncio
async def test_register_and_unregister(fake_redis):
    manager = ConnectionManager("redis://test")
    await manager.wait_ready()
    ws = DummyWebSocket()
    conn = WsConnection(websocket=ws, id="agent1")
    await manager.register(conn)
    assert await manager.get("agent1") is conn
    assert await fake_redis.get("connection:agent1") == conn.serialize()

    await manager.unregister(conn)
    assert await manager.get("agent1") is None
    assert await fake_redis.get("connection:agent1") is None
    assert ws.closed


@pytest.mark.asyncio
async def test_concurrent_register_unregister(fake_redis):
    manager = ConnectionManager("redis://test")
    await manager.wait_ready()
    ws1, ws2 = DummyWebSocket(), DummyWebSocket()
    c1 = WsConnection(websocket=ws1, id="a1")
    c2 = WsConnection(websocket=ws2, id="a2")

    await asyncio.gather(manager.register(c1), manager.register(c2))
    conns = await manager.list_all()
    assert set(conns.keys()) == {"a1", "a2"}

    await asyncio.gather(manager.unregister(c1), manager.unregister(c2))
    assert await manager.list_all() == {}
