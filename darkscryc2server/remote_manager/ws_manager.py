import json
from fastapi import WebSocket, WebSocketDisconnect
from ..Models.remote_tools_schemas import ManagerAction, ManagerRequestWs, ManagerResponse
from ..settings.config import internalapplogger as logger

async def manager_ws_endpoint(websocket: WebSocket):
    """
    The main WebSocket endpoint for manager requests.
    """
    await websocket.accept()
    server = websocket.app.state.server
    try:
        while True:
            raw = await websocket.receive_text()
            try:
                data = json.loads(raw)
                req = ManagerRequestWs(**data)
            except Exception as e:
                error_resp = ManagerResponse(success=False, error=f"Invalid request: {e}")
                await websocket.send_text(error_resp.model_dump_json())
                continue

            if req.action == ManagerAction.GET_CONNECTIONS:
                conns = list(server.connection_manager.get_all_connections().keys())
                resp = ManagerResponse(success=True, data={"connections": conns})
                await websocket.send_text(resp.model_dump_json())

            elif req.action == ManagerAction.SEND_COMMAND:
                if not req.conn_id or not req.command:
                    error_resp = ManagerResponse(success=False, error="Missing conn_id or command")
                    await websocket.send_text(error_resp.model_dump_json())
                    continue

                conn = server.connection_manager.get_connection(req.conn_id)
                if not conn:
                    error_resp = ManagerResponse(success=False, error=f"No such connection: {req.conn_id}")
                    await websocket.send_text(error_resp.model_dump_json())
                    continue

                try:
                    result_bytes = await conn.send_command(req.command.encode("utf-8"))
                    if result_bytes is None:
                        resp = ManagerResponse(success=False, error="No response or connection closed")
                    else:
                        resp = ManagerResponse(
                            success=True,
                            data={"result": result_bytes.decode('utf-8', 'ignore')}
                        )
                    await websocket.send_text(resp.model_dump_json())
                except Exception as ex:
                    error_resp = ManagerResponse(success=False, error=str(ex))
                    await websocket.send_text(error_resp.model_dump_json())
            else:
                error_resp = ManagerResponse(success=False, error=f"Unknown action: {req.action}")
                await websocket.send_text(error_resp.model_dump_json())

    except WebSocketDisconnect:
        logger.info("[manager_ws] WebSocket disconnected.")
    except Exception as ex:
        logger.exception(f"[manager_ws] Error: {ex}")
    finally:
        await websocket.close()
