from ninja import NinjaAPI
from .agents import AgentsApi
from .test import TestApi

#api manager
api_ninja = NinjaAPI()

#routers
agents_manager = AgentsApi()
test_api = TestApi()

api_ninja.add_router("/agents", router=agents_manager.router)
api_ninja.add_router("/test", test_api.router)
