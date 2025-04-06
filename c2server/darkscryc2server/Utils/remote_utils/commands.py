import aiohttp
from pydantic import ValidationError
from ...Models.remote_tools_schemas import ManagerResponse
from json import loads
from os import getenv

_session = None
def session():
    global _session
    if _session is None:
        _session = aiohttp.ClientSession()
    return _session


async def remote_get_connections(host: str = None, port: int = 9100) -> ManagerResponse:
    """
    Retrieve the list of connections. Return a ManagerResponse object.
    Raise exceptions for network or parse errors.
    """
    if host is None:
        host = getenv("C2_SERVER_HOST", "127.0.0.1")
    r = await session().get(url="http://{}:{}/api/connections".format(host,port))
    resp_dict = await r.json()
    # Now parse into a ManagerResponse
    try:
        mgr_resp = ManagerResponse(**resp_dict)
        return mgr_resp
    except ValidationError as ve:
        return ManagerResponse(success=False, error=ve.json())


async def remote_send_command(conn_id: str, command: str, host: str = "127.0.0.1", port: int = 9100, _parse_data=False) -> ManagerResponse:
    """
    Instruct a specific connection to run 'command'.
    Return a ManagerResponse object (with success/data/error).
    """
    req = {
        "action": "send_command",
        "conn_id": conn_id,
        "command": command,
    }
    r = await session().post(url="http://{}:{}/api/send_command".format(host,port), json=req)
    resp_dict = await r.json()
    
    try:
        mgr_resp = ManagerResponse(**resp_dict)
        if _parse_data:
            if isinstance(mgr_resp.data["result"], str):
                mgr_resp.data = loads(mgr_resp.data["result"])
            else:
                mgr_resp.data = mgr_resp.data["result"]
        return mgr_resp
    except ValidationError as ve:
        return ManagerResponse(success=False, error=ve.json())
