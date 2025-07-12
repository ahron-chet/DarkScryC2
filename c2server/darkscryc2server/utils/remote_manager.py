from os import getenv

import aiohttp

from ..models.messages import AgentResponse, CommandMessage

_session = None


def session():
    global _session
    if _session is None:
        _session = aiohttp.ClientSession()
    return _session


async def remote_get_connections(host: str = None, port: int = 9100) -> list:
    """
    Retrieve the list of connections. Return a ManagerResponse object.
    Raise exceptions for network or parse errors.
    """
    if host is None:
        host = getenv("C2_SERVER_HOST", "127.0.0.1")
    r = await session().get(url="http://{}:{}/api/connections".format(host, port))
    return await r.json()


async def remote_send_command(
    agent_id: str,
    command: str,
    args: dict | None = None,
    host: str = None,
    port: int = 9100,
) -> AgentResponse:
    """
    Instruct a specific connection to run 'command'.
    """
    if host is None:
        host = getenv("C2_SERVER_HOST", "127.0.0.1")
    req = CommandMessage(command=command, args=args).model_dump(exclude_none=True)
    try:
        r = await session().post(
            url="http://{}:{}/command/{}".format(host, port, agent_id), json=req
        )
        resp_dict = await r.json()
        return AgentResponse(**resp_dict)
    except Exception as e:
        raise e
