import asyncio
from typing import Dict, Optional

from .redis_manager import RedisManager
from .wsbased_connection import WsConnection
from ..settings.config import internalapplogger as logger
from pickle import dumps, loads

class ConnectionManager:
    def __init__(self, redis_url: str) -> None:
        self.connections: Dict[str, WsConnection] = {}
        self.redis_manager = RedisManager(redis_url)
        self._redis_connect_task = asyncio.create_task(self._async_connect())

    async def _async_connect(self):
        try:
            await self.redis_manager.connect()
        except RuntimeError as e:
            logger.error(f"Failed to connect to Redis: {e}")

    async def wait_until_connected(self):
        await self._redis_connect_task

    async def register(self, connection: WsConnection) -> None:
        self.connections[connection.id] = connection
        logger.info(f"Registered connection {connection.id} from {connection.address}")
        try:
            await self.redis_manager.set(
                key=f"connection:{connection.id}",
                value=dumps({"address": str(connection.address), "type": "WSPROTO"})
            )
        except RuntimeError as e:
            logger.error(f"Redis set error: {e}")

    async def unregister(self, connection: WsConnection) -> None:
        conn_id = connection.id
        if conn_id in self.connections:
            await connection.close()
            del self.connections[conn_id]
            logger.info(f"Unregistered connection {conn_id}")
            try:
                await self.redis_manager.delete(key=f"connection:{conn_id}")
            except RuntimeError as e:
                logger.error(f"Redis delete error: {e}")

    def get_connection(self, conn_id: str) -> Optional[WsConnection]:
        return self.connections.get(conn_id)

    def get_all_connections(self) -> Dict[str, WsConnection]:
        return self.connections

    async def get_all_connections_redis(self) -> Dict[str, dict]:
        return {i: loads(await self.redis_manager.get(f"connection:{i}")) for i in self.connections}

    async def close_all_connections(self) -> None:
        for conn in list(self.connections.values()):
            await self.unregister(conn)
        logger.info("All connections have been closed.")
