import asyncio
from DarkScryC2Server.Server.Server import Server

server_manager = Server()
asyncio.run(server_manager.start())