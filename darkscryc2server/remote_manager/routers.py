from fastapi import APIRouter, Body, HTTPException, Request
from ..Models.remote_tools_schemas import ManagerSendCommand, ManagerResponse
from ..Managers.connection_manager import Connection
from ..Managers.wsbased_connection import WsConnection
from ..Server import Server
from ..settings.config import internalapplogger as logger
from json import loads

router = APIRouter()

from fastapi import Request

@router.get("/connections", summary="List all active connections")
async def list_connections(request:Request):
    """
    Returns a list of current connection IDs.
    """
    server = _server(request)
    conns = await server.connection_manager.get_all_connections_redis()
    return ManagerResponse(success=True, data={"connections": conns})



@router.post("/send_command", summary="Send a command to a specific connection", response_model=ManagerResponse)
async def send_command(
    request: Request,
    ManagerRequest: ManagerSendCommand
):
    """
    Send a command to a given connection (by ID).
    """
    server = _server(request)
    conn = server.connection_manager.get_connection(ManagerRequest.conn_id)
    if not conn:
        logger.warning(f"Connection not found: {ManagerRequest.conn_id}")
        raise HTTPException(status_code=404, detail=f"No such connection: {ManagerRequest.conn_id}")

    try:
        if isinstance(conn, WsConnection):
            result_bytes = await conn.send_and_receive(ManagerRequest.command)
        else:
            result_bytes = await conn.send_command(ManagerRequest.command.encode("utf-8"))
        if result_bytes is None:
            raise HTTPException(status_code=400, detail="No response or connection closed")
        return ManagerResponse(success=True, data={"result": loads(result_bytes)})
    except Exception as e:
        logger.exception(f"Error sending command: {e}")
        raise HTTPException(status_code=500, detail=str(e))    

def _server(request) -> Server:
    return request.app.state.server


