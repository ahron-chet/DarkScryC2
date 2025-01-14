from fastapi import APIRouter, Body, HTTPException, Request

from ..Server import Server
from ..settings.config import internalapplogger as logger

router = APIRouter()

from fastapi import Request

@router.get("/connections", summary="List all active connections")
def list_connections(request: Request):
    """
    Returns a list of current connection IDs.
    """
    server = _server(request)
    conns = list(server.connection_manager.get_all_connections().keys())
    return {"connections": conns}


@router.post("/send_command", summary="Send a command to a specific connection")
async def send_command(
    request: any,
    conn_id: str = Body(...),
    command: str = Body(...),
):
    """
    Send a command to a given connection (by ID).
    """
    server = _server(request)
    conn = server.connection_manager.get_connection(conn_id)
    if not conn:
        logger.warning(f"Connection not found: {conn_id}")
        raise HTTPException(status_code=404, detail=f"No such connection: {conn_id}")

    try:
        result_bytes = await conn.send_command(command.encode("utf-8"))
        if result_bytes is None:
            raise HTTPException(status_code=400, detail="No response or connection closed")
        return {"result": result_bytes.decode("utf-8", "ignore")}
    except Exception as e:
        logger.exception(f"Error sending command: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

def _server(request) -> Server:
    return request.app.state.server
