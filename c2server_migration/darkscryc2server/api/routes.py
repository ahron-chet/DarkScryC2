from fastapi import APIRouter, HTTPException, Request

from ..core.connection import ConnectionManager
from ..models.messages import CommandMessage

router = APIRouter()


@router.get("/connections")
async def list_connections(request: Request):
    manager: ConnectionManager = request.app.state.conn_manager
    return list((await manager.list_all()).keys())


@router.post("/command/{agent_id}")
async def send_command(request: Request, agent_id: str, msg: CommandMessage):
    manager: ConnectionManager = request.app.state.conn_manager
    conn = await manager.get(agent_id)
    if not conn:
        raise HTTPException(status_code=404, detail="Agent not found")
    result = await conn.send_and_receive(msg.model_dump_json())
    return {"result": result}
