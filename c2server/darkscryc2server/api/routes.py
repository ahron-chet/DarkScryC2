from json import loads

from fastapi import APIRouter, HTTPException, Request

from ..core.connection import ConnectionManager
from ..models.messages import AgentResponse, CommandMessage

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


@router.get("/connections/{agent_id}")
async def get_connection(request: Request, agent_id: str):
    """Return details for a single active connection."""
    manager = _server(request)
    conn = await manager.get(agent_id)
    if not conn:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"address": str(conn.address), "type": "ws"}


@router.post("/command/{agent_id}", response_model=AgentResponse)
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
    AgentResponse
        The agent's structured response.
    """
    manager = _server(request)
    conn = await manager.get(agent_id)
    if not conn:
        raise HTTPException(status_code=404, detail="Agent not found")

    try:
        result_bytes = await conn.send_and_receive(msg.model_dump_json())
        if result_bytes is None:
            raise HTTPException(
                status_code=400, detail="No response or connection closed"
            )
        try:
            response_data = loads(result_bytes)
            return AgentResponse(**response_data)
        except Exception as parse_err:
            raise HTTPException(
                status_code=500,
                detail=f"Invalid response format: {parse_err}"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def _server(request: Request) -> ConnectionManager:
    return request.app.state.conn_manager
