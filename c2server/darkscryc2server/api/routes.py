from fastapi import APIRouter, HTTPException, Request

from ..core.connection import ConnectionManager
from ..models.messages import CommandMessage

router = APIRouter()


@router.get("/connections")
async def list_connections(request: Request):
    """Return a list of IDs for all active agent connections.

    Parameters
    ----------
    request: Request
        Incoming request used to access the connection manager stored in the
        application state.

    Returns
    -------
    list[str]
        Identifiers of all connected agents.
    """
    manager = _server(request)
    conns = await manager.list_all()
    return list(conns.keys())


@router.post("/command/{agent_id}")
async def send_command(request: Request, agent_id: str, msg: CommandMessage):
    """Send a command message to a specific agent and return its response.

    Parameters
    ----------
    request: Request
        FastAPI request instance used to access the connection manager.
    agent_id: str
        Identifier of the target agent connection.
    msg: CommandMessage
        Message to send to the agent.

    Returns
    -------
    dict
        A mapping with the key ``"result"`` containing the agent's response.
    """
    manager = _server(request)
    conn = await manager.get(agent_id)
    if not conn:
        raise HTTPException(status_code=404, detail="Agent not found")
    result = await conn.send_and_receive(msg.model_dump_json())
    return {"result": result}


def _server(request: Request) -> ConnectionManager:
    return request.app.state.conn_manager
