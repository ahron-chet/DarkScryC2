import asyncio
import time
import uuid
from typing import Dict, Optional

from ..settings.config import (
    internalapplogger as logger
)
from .connection_manager import ConnectionManager, Connection




class KeepAliveManager:
    def __init__(self, connection_manager: ConnectionManager, interval: int = 1200) -> None:
        self.connection_manager = connection_manager
        self.interval = interval

    async def start(self) -> None:
        while True:
            await asyncio.sleep(self.interval)
            connections = list(self.connection_manager.get_all_connections().values())
            tasks = [self._ping_and_update(conn) for conn in connections]
            try:
                await asyncio.gather(*tasks, return_exceptions=True)
            except Exception as e:
                logger.error(f"KeepAliveManager error: {e}")

    async def ping(self, connection: Connection) -> bool:
        try:
            await connection._send(b"PING") 
            return True
        except Exception as e:
            logger.error(f"ping failed for {connection.id}: {e}")
            return False

    async def _ping_and_update(self, connection: Connection) -> None:
        ok = await self.ping(connection)
        if ok:
            try:
                timestamp = int(time.time())
                self.connection_manager.redis_manager.set(
                    key=f"connection:{connection.id}:last_ping",
                    value=str(timestamp)
                )
                logger.debug(f"KeepAlive ping OK for {connection.id}")
            except RuntimeError as e:
                logger.error(f"Redis error updating last_ping for {connection.id}: {e}")
        else:
            logger.warning(f"Connection {connection.id} failed keep-alive ping")
            self.connection_manager.unregister(connection)
