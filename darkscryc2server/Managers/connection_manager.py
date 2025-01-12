import asyncio
import uuid
from typing import Dict, Optional
import struct

from ..settings.config import internalapplogger as logger
from ..Models.protocols import SOCKET_BASE_MESSAGE_HEADER, SIZE_OF_SOCKET_BASE_MESSAGE_HEADER
from ..Utils.tools import pack_base_header, unpack_base_header
from .redis_manager import RedisManager
from ..Cryptography.Symetric import AesCrypto


_MAX_LENGTH_FOR_SYNC = 65536

# Example opcodes
OPCODE_CMD_REQUEST  = 3
OPCODE_CMD_RESPONSE = 4

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

        # For concurrency: Store pending requests by request_id -> Future
        self._pending_requests: Dict[int, asyncio.Future] = {}
        # We'll just keep a small 16-bit auto-increment
        self._next_request_id: int = 1

        # A running flag for the read loop
        self._running = True

    # ------------------------------------------------------
    # 1) The base send/receive for the "outer" message
    # ------------------------------------------------------
    async def send(self, message: bytes, _enc: bool = True) -> None:
        """
        1) Possibly encrypt
        2) Build a SOCKET_BASE_MESSAGE_HEADER w/ payload_length
        3) pack_base_header => writer.write => drain
        """
        if not message:
            return

        use_async_enc = (len(message) > _MAX_LENGTH_FOR_SYNC)
        if _enc:
            message = await self.aes_manager.encrypt(message, use_async_enc)

        # Build the 'outer' header (c_uint32 for length)
        headers = SOCKET_BASE_MESSAGE_HEADER()
        headers.payload_length = len(message)
        self.writer.write(pack_base_header(headers))
        self.writer.write(message)
        await self.writer.drain()

    async def receive(self, _enc: bool = True) -> Optional[bytes]:
        """
        1) Read 4 bytes => length
        2) Read that many => decrypt => return plaintext
        Returns None if incomplete or EOF
        """
        try:
            header_data = await self.reader.readexactly(SIZE_OF_SOCKET_BASE_MESSAGE_HEADER)
        except asyncio.IncompleteReadError:
            return None

        headers = unpack_base_header(header_data)
        try:
            msg = await self.reader.readexactly(headers.payload_length)
        except asyncio.IncompleteReadError:
            return None

        if not _enc:
            return msg

        use_async = (headers.payload_length > _MAX_LENGTH_FOR_SYNC)
        plaintext = await self.aes_manager.decrypt(msg, use_async)
        return plaintext

    # ------------------------------------------------------
    # 2) The single read loop in start()
    # ------------------------------------------------------
    async def start(self) -> None:
        """
        A single read loop that repeatedly calls `receive()`,
        then parses the 'inner' message => [opcode(1), request_id(2), body_len(4), body].
        If it's a response, we set the correct future's result.
        Otherwise we handle or ignore.
        """
        logger.debug(f"[Connection {self.id}] Starting read loop.")
        try:
            while self._running and not self.writer.is_closing():
                plaintext = await self.receive(_enc=True)
                if not plaintext:
                    logger.debug(f"[Connection {self.id}] EOF or partial read => exit.")
                    break

                # parse [1 byte opcode, 2 bytes request_id, 4 bytes body_len, body]
                if len(plaintext) < 1 + 2 + 4:
                    logger.debug("Malformed internal message (too short).")
                    continue

                opcode = plaintext[0]
                # request_id = 2 bytes => we assume big-endian or little-endian. Let's do big-endian:
                request_id = int.from_bytes(plaintext[1:3], 'big')
                body_len = int.from_bytes(plaintext[3:7], 'big')

                if len(plaintext) < (7 + body_len):
                    logger.debug("Truncated body => ignoring.")
                    continue

                body = plaintext[7:7+body_len]

                if opcode == OPCODE_CMD_RESPONSE:
                    # This is presumably the response for a previously sent command
                    fut = self._pending_requests.pop(request_id, None)
                    if fut and not fut.done():
                        fut.set_result(body)
                else:
                    # Possibly a request from the client, or a ping, or something else
                    logger.debug(f"Received unsolicited opcode={opcode} req_id={request_id} len={body_len}")
                    # You can handle if needed
        except asyncio.CancelledError:
            logger.debug(f"[Connection {self.id}] Task canceled.")
        except Exception as e:
            logger.error(f"[Connection {self.id}] Read loop error: {e}")
        finally:
            logger.debug(f"[Connection {self.id}] Exiting read loop.")
            self._running = False
            self.close()

    # ------------------------------------------------------
    # 3) Concurrency-safe send_command
    # ------------------------------------------------------
    async def send_command(self, command_data: bytes) -> Optional[bytes]:
        """
        1) We'll pick the next request_id
        2) Build [opcode=OPCODE_CMD_REQUEST(3), request_id(2), body_len(4), body=command_data]
        3) Send it with self.send
        4) Create a Future, store in _pending_requests[request_id]
        5) Wait for read loop to produce a response => fut result
        """
        loop = asyncio.get_running_loop()
        fut = loop.create_future()

        # simple approach: wrap if >65535
        req_id = self._next_request_id
        self._next_request_id = (self._next_request_id + 1) % 65536

        self._pending_requests[req_id] = fut

        body_len = len(command_data)
        opcode = OPCODE_CMD_REQUEST
        # Pack the 'inner' message
        # opcode(1), request_id(2, big-endian), body_len(4, big-endian), body
        header = bytearray(1 + 2 + 4)
        header[0] = opcode
        header[1:3] = req_id.to_bytes(2, 'big')
        header[3:7] = body_len.to_bytes(4, 'big')

        plaintext = header + command_data

        # Send
        await self.send(plaintext, _enc=True)

        # Wait for the response
        result = await fut
        return result

    def close(self) -> None:
        """
        Stop reading, close the writer if not closed.
        """
        self._running = False
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