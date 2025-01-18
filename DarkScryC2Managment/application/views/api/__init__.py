from ninja import NinjaAPI
from .agents import AgentsApi
api_ninja = NinjaAPI()

agents_manager = AgentsApi()

api_ninja.add_router("agents/", agents_manager.router)