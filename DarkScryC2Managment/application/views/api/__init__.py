from ninja import NinjaAPI
from .agents import AgentsApi
from .test import TestApi as TestApi

from .modules.collection import mashine
from . import tasks

#api manager
api_ninja = NinjaAPI()

#routers
agents_manager = AgentsApi()
test_api = TestApi()
task_manager_api = tasks.TaskApi()

collection_mashine = mashine.MashineCollection()

api_ninja.add_router("/agents", router=agents_manager.router)
# api_ninja.add_router("/test", test_api.router)
api_ninja.add_router("/tasks", task_manager_api.router)

api_ninja.add_router("/collection/machine", collection_mashine.router)


