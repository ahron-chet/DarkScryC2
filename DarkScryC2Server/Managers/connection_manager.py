import asyncio
import uuid
from typing import Dict, Optional

from ..settings.config import internalapplogger as logger
from ..Models.protocols import SOCKET_BASE_MESSAGE_HEADER, SIZE_OF_SOCKET_BASE_MESSAGE_HEADER
from ..Utils.tools import pack_base_header, unpack_base_header
from .redis_manager import RedisManager
from ..Cryptography.Symetric import AesCrypto



class Connection:
    def __init__(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
        aes_manager: AesCrypto,
        uid: uuid.UUID
    ) -> None:
        self.id = str(uid)
        self.reader = reader
        self.writer = writer
        self.address = writer.get_extra_info("peername")
        self.aes_manager = aes_manager

    async def send(self, message: bytes, _enc: bool = True) -> None:
        if not message:
            return
        if _enc:
            message = await self.aes_manager.encrypt(message)

        headers = SOCKET_BASE_MESSAGE_HEADER()
        headers.payload_length = len(message)
        self.writer.write(pack_base_header(headers))
        self.writer.write(message)
        await self.writer.drain()

    async def receive(self, _enc: bool = True) -> Optional[bytes]:
        try:
            header_data = await self.reader.readexactly(SIZE_OF_SOCKET_BASE_MESSAGE_HEADER)
        except asyncio.IncompleteReadError:
            return None

        headers = unpack_base_header(header_data)
        try:
            msg = await self.reader.readexactly(headers.payload_length)
            return await self.aes_manager.decrypt(msg) if _enc else msg
        except asyncio.IncompleteReadError:
            return None
        
    async def send_command(self, command:str):
        await self.send(command.encode())
        return await self.receive()

    async def start(self) -> None:
        logger.debug(f"[Connection {self.id}] Session started. No receiving loop.")
        try:
            while not self.writer.is_closing():
                await asyncio.sleep(5)
            logger.debug(f"[Connection {self.id}] Writer closed, ending session.")
        except asyncio.CancelledError:
            logger.debug(f"[Connection {self.id}] Task canceled, closing connection.")
        finally:
            self.close()


    def close(self) -> None:
        if not self.writer.is_closing():
            self.writer.close()

class ConnectionManager:
    def __init__(self, redis_url: str) -> None:
        self.connections: Dict[str, Connection] = {}
        self.redis_manager = RedisManager(redis_url)
        self._redis_connect_task = asyncio.create_task(self._async_connect())

    async def _async_connect(self):
        """
        Private async method that attempts to connect to Redis.
        """
        try:
            await self.redis_manager.connect()
        except RuntimeError as e:
            logger.error(f"Failed to connect to Redis: {e}")

    async def wait_until_connected(self):
        """
        Optional method to wait for the Redis connection to finish.
        If you want to ensure the connection is ready, call:
           await manager.wait_until_connected()
        """
        await self._redis_connect_task

    async def register(self, connection: Connection) -> None:
        self.connections[connection.id] = connection
        logger.info(f"Registered connection {connection.id} from {connection.address}")
        try:
            await self.redis_manager.set(
                key=f"connection:{connection.id}",
                value=str(connection.address)
            )
        except RuntimeError as e:
            logger.error(f"Redis set error: {e}")

    async def unregister(self, connection: Connection) -> None:
        conn_id = connection.id
        if conn_id in self.connections:
            connection.close()
            del self.connections[conn_id]
            logger.info(f"Unregistered connection {conn_id}")
            try:
                await self.redis_manager.delete(key=f"connection:{conn_id}")
                await self.redis_manager.delete(key=f"connection:{conn_id}:last_ping")
            except RuntimeError as e:
                logger.error(f"Redis delete error: {e}")

    def get_connection(self, conn_id: str) -> Optional[Connection]:
        return self.connections.get(conn_id)

    def get_all_connections(self) -> Dict[str, Connection]:
        return  self.connections

    async def close_all_connections(self) -> None:
        for conn in list(self.connections.values()):
            await self.unregister(conn)
        logger.info("All connections have been closed.")   