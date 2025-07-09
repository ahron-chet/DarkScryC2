from __future__ import annotations

import json
from fastapi import WebSocket, WebSocketDisconnect, Depends

from ..connections.manager import ConnectionManager
from ..models.messages import ManagerAction, ManagerRequestWs, ManagerResponse


async def manager_ws_endpoint(websocket: WebSocket, manager: ConnectionManager = Depends()):
    await websocket.accept()
    try:
        while True:
            raw = await websocket.receive_text()
            try:
                req = ManagerRequestWs.model_validate_json(raw)
            except Exception as exc:
                await websocket.send_text(
                    ManagerResponse(success=False, error=f"Invalid request: {exc}").model_dump_json()
                )
                continue
            if req.action == ManagerAction.GET_CONNECTIONS:
                conns = list(manager.list_all().keys())
                await websocket.send_text(
                    ManagerResponse(success=True, data={"connections": conns}).model_dump_json()
                )
            elif req.action == ManagerAction.SEND_COMMAND:
                if not req.conn_id or not req.command:
                    await websocket.send_text(
                        ManagerResponse(success=False, error="Missing conn_id or command").model_dump_json()
                    )
                    continue
                conn = manager.get(req.conn_id)
                if not conn:
                    await websocket.send_text(
                        ManagerResponse(success=False, error=f"No such connection: {req.conn_id}").model_dump_json()
                    )
                    continue
                try:
                    result = await conn.send_and_receive(req.command)
                    await websocket.send_text(
                        ManagerResponse(success=True, data={"result": result}).model_dump_json()
                    )
                except Exception as exc:
                    await websocket.send_text(
                        ManagerResponse(success=False, error=str(exc)).model_dump_json()
                    )
            else:
                await websocket.send_text(
                    ManagerResponse(success=False, error=f"Unknown action: {req.action}").model_dump_json()
                )
    except WebSocketDisconnect:
        pass
    finally:
        await websocket.close()
