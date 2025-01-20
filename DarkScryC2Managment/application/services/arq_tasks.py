from darkscryc2server.Utils.remote_utils.commands import remote_send_command
import time

async def remote_send_command_task(ctx, agent_id: str, command: str, _action_name:str):
    result = await remote_send_command(conn_id=agent_id, command=command)
    if not result.success:
        raise Exception(result.error)
    return result.model_dump()