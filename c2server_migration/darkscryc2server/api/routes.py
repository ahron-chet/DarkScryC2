from fastapi import APIRouter, HTTPException, Depends
from ..connections.manager import ConnectionManager
from ..models.messages import CommandMessage

router = APIRouter()


def get_manager(router: APIRouter) -> ConnectionManager:
    return router.dependencies[0]

@router.get("/connections")
async def list_connections(manager: ConnectionManager = Depends()):
    return list(manager.list_all().keys())

@router.post("/command/{agent_id}")
async def send_command(agent_id: str, msg: CommandMessage, manager: ConnectionManager = Depends()):
    conn = manager.get(agent_id)
    if not conn:
        raise HTTPException(status_code=404, detail="Agent not found")
    result = await conn.send_and_receive(msg.json())
    return {"result": result}
