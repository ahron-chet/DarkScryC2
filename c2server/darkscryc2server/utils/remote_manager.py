import aiohttp
from ..models.messages import AgentResponse
from os import getenv
from ..models.messages import CommandMessage, AgentResponse, CommandIdentifiers

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
    r = await session().get(url="http://{}:{}/api/connections".format(host,port))
    return await r.json()



async def remote_send_command(agent_id: str, action_id: CommandIdentifiers, command: dict=None, host: str = None, port: int = 9100) -> AgentResponse:
    """
    Instruct a specific connection to run 'command'.
    """
    if host is None:
        host = getenv("C2_SERVER_HOST", "127.0.0.1")
    req = CommandMessage(command=command, action_id=action_id).model_dump(exclude_none=True)
    try:
        r = await session().post(url="http://{}:{}/command/{}".format(host,port,agent_id), json=req)
        resp_dict = await r.json()
        return AgentResponse(**resp_dict)
    except Exception as e:
        raise e

