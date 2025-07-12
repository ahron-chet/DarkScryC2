from os import getenv

import aiohttp

from ..models.messages import AgentResponse, CommandIdentifiers, CommandMessage, ServerError

_session = None


def session():
    global _session
    if _session is None:
        _session = aiohttp.ClientSession()
    return _session


async def remote_get_connections(host: str = None, port: int = 9100) -> list:
    """
    Retrieve the list of connections. Return a list of connected agents.
    Raise exceptions for network or parse errors.
    """
    if host is None:
        host = getenv("C2_SERVER_HOST", "127.0.0.1")
    r = await session().get(url=f"http://{host}:{port}/connections")
    return await r.json()


async def remote_get_connection(
    agent_id: str, host: str | None = None, port: int = 9100
) -> dict | None:
    """Retrieve details for a single connection."""
    if host is None:
        host = getenv("C2_SERVER_HOST", "127.0.0.1")
    r = await session().get(url=f"http://{host}:{port}/connections/{agent_id}")
    if r.status == 404:
        return None
    return await r.json()


async def remote_send_command(
    agent_id: str,
    action_id: CommandIdentifiers,
    command: dict = None,
    host: str = None,
    port: int = 9100,
) -> AgentResponse:
    """
    Instruct a specific connection to run 'command'.
    """
    if host is None:
        host = getenv("C2_SERVER_HOST", "127.0.0.1")

    req = CommandMessage(command=command, action_id=action_id).model_dump(
        exclude_none=True
    )

    try:
        r = await session().post(
            url=f"http://{host}:{port}/command/{agent_id}", json=req
        )
        if r.status == 404:
            return AgentResponse(success=False, data={"type":"Server Error"}, error=f"{agent_id} not found or not connected")
        resp_dict = await r.json()
        return AgentResponse(**resp_dict)
    except Exception as e:
        return AgentResponse(success=False, data={"type":"Server Error"}, error=str(e))
