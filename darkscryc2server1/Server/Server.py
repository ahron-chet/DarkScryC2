import asyncio

from ..settings.config import (
    SERVER_HOST,
    SERVER_PORT,
    internalapplogger as logger
)
# from ..Managers.keep_alive_manager import KeepAliveManager
from ..Managers.connection_manager import Connection, ConnectionManager
from ..settings.config import REDIS_URI
from ..Cryptography.Asymetric import RSAManager
from ..Cryptography.Symetric import AesCrypto
from ..settings.config import internalapplogger as logger, PRIVATE_KEY_PATH
from ..Models.schemas import AgentConnection
from json import loads

class Server:
    def __init__(self) -> None:
        self.connection_manager = ConnectionManager(REDIS_URI)
        self._rsa_manager = RSAManager(PRIVATE_KEY_PATH)

    async def start(self) -> None:
        await self.connection_manager.wait_until_connected()
        try:
            server = await asyncio.start_server(
                self._handle_client,
                SERVER_HOST,
                SERVER_PORT
            )
            logger.info(f"Server started on {SERVER_HOST}:{SERVER_PORT}")
            async with server:
                await server.serve_forever()
        except Exception as e:
            logger.error(f"Server failed to start: {e}")

    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        try:
            conn_id, aes_manager = await self._perform_handshake(reader, writer)
            if not conn_id or not aes_manager:
                return
            
            connection = Connection(reader, writer, aes_manager, conn_id)
            await self.connection_manager.register(connection)
        except Exception as e:
            logger.error(f"Handshake error: {e}")
            writer.close()
            return
        try:
            await connection.start()
        except Exception as e:
            logger.error(f"Connection {connection.id} error: {e}")
        finally:
            await self.connection_manager.unregister(connection)

    async def _perform_handshake(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter
    ):
        try:
            raw_connection = await reader.readexactly(256)
        except asyncio.IncompleteReadError:
            logger.warning("Client disconnected before sending handshake.")
            writer.close()
            return None, None

        try:
            decrypted_data = await asyncio.to_thread(self._rsa_manager.decrypt_data, raw_connection)
        except Exception as e:
            logger.error(f"RSA decryption failed: {e}")
            writer.close()
            return None, None

        try:
            connect_data = AgentConnection(**loads(decrypted_data))
            aes =  AesCrypto(connect_data.key, None)
            aes.set_iv(key=connect_data.key)
            return str(connect_data.agent_id), aes
        except Exception as e:
            logger.error(f"Invalid handshake data: {e}")
            writer.close()
            return None, None
