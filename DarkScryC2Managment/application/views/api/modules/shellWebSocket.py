# yourapp/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import InMemoryChannelLayer

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
        data = json.loads(data)
        command = data.get("command")
        # Do shell logic or dispatch to a worker, etc.
        result = f"You sent the command: {command}"
        # Echo back:
        await self.send(json.dumps({
            "message": result
        }))