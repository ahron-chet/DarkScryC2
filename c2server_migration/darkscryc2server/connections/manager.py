from __future__ import annotations

import asyncio
from typing import Dict

from .redis import RedisClient
from .ws import WsConnection

class ConnectionManager:
    def __init__(self, redis_url: str) -> None:
        self.redis = RedisClient(redis_url)
        self.connections: Dict[str, WsConnection] = {}
        self._connect_task = asyncio.create_task(self.redis.connect())

    async def wait_ready(self) -> None:
        await self._connect_task

    async def register(self, conn: WsConnection) -> None:
        await self.wait_ready()
        self.connections[conn.id] = conn
        await self.redis.set(f"connection:{conn.id}", conn.serialize())

    async def unregister(self, conn: WsConnection) -> None:
        await self.wait_ready()
        self.connections.pop(conn.id, None)
        await conn.close()
        await self.redis.delete(f"connection:{conn.id}")

    def get(self, conn_id: str) -> WsConnection | None:
        return self.connections.get(conn_id)

    def list_all(self) -> Dict[str, WsConnection]:
        return dict(self.connections)
