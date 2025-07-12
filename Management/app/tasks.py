"""Background job functions used with arq."""

from darkscryc2server.models.messages import CommandIdentifiers
from darkscryc2server.utils.remote_manager import remote_send_command


async def remote_send_command_task(ctx, agent_id: str, action_id: CommandIdentifiers, command:dict=None):
    result = await remote_send_command(
        agent_id=agent_id, command=command, action_id=action_id
    )
    return result.model_dump()
