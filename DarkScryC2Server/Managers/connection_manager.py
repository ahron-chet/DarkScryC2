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
            message = self.aes_manager.encrypt(message)

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
            return self.aes_manager.decrypt(msg) if _enc else msg
        except asyncio.IncompleteReadError:
            return None
        
    async def send_command(command:str):
        pass

    async def start(self) -> None:
        logger.debug(f"[Connection {self.id}] Started listening for messages.")   
        while True:
            data = await self.receive()
            if data is None:
                logger.debug(f"[Connection {self.id}] No data received or connection closed.")
                break
            await self.onMessage(data)
        self.close()
        logger.debug(f"[Connection {self.id}] Connection closed.")

    async def onMessage(self, data: bytes) -> None:
        logger.info(f"[Connection {self.id}] Received data: {data}")
        await self.send(b"hello from python"*200)

    def close(self) -> None:
        if not self.writer.is_closing():
            self.writer.close()

class ConnectionManager:
    def __init__(self, redis_url: str) -> None:
        self.connections: Dict[str, Connection] = {}
        self.redis_manager = RedisManager(redis_url)
        try:
            self.redis_manager.connect()
        except RuntimeError as e:
            logger.error(f"Failed to connect to Redis: {e}")

    def register(self, connection: Connection) -> None:
        self.connections[connection.id] = connection
        logger.info(f"Registered connection {connection.id} from {connection.address}")
        try:
            self.redis_manager.set(
                key=f"connection:{connection.id}",
                value=str(connection.address)
            )
        except RuntimeError as e:
            logger.error(f"Redis set error: {e}")

    def unregister(self, connection: Connection) -> None:
        conn_id = connection.id
        if conn_id in self.connections:
            connection.close()
            del self.connections[conn_id]
            logger.info(f"Unregistered connection {conn_id}")
            try:
                self.redis_manager.delete(key=f"connection:{conn_id}")
                self.redis_manager.delete(key=f"connection:{conn_id}:last_ping")
            except RuntimeError as e:
                logger.error(f"Redis delete error: {e}")

    def get_connection(self, conn_id: str) -> Optional[Connection]:
        return self.connections.get(conn_id)

    def get_all_connections(self) -> Dict[str, Connection]:
        return self.connections

    def close_all_connections(self) -> None:
        for conn in list(self.connections.values()):
            self.unregister(conn)
        logger.info("All connections have been closed.")   