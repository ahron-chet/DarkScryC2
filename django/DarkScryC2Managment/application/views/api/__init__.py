from ninja import NinjaAPI
from .agents import AgentsApi
from .test import TestApi as TestApi

from .agents_modules.collection import mashine
from .agents_modules.collection import files
from .agents_modules.collection import passwords
from .agents_modules.collection import processe
from .agents_modules.execution import shell

from . import tasks
from .auth import AuthV2
from . import users

#api manager
api_ninja = NinjaAPI()

#routers
authv2 = AuthV2()
agents_manager = AgentsApi()
test_api = TestApi()
task_manager_api = tasks.TaskApi()
user_api = users.UserApi()

collection_mashine = mashine.MashineCollection()
collection_files = files.FileCollection()
collection_password = passwords.PasswordCollection()
collection_processe = processe.ProcessCollection()

execution_shell = shell.ShellExecution()

api_ninja.add_router("", router=authv2.router)
api_ninja.add_router("", router=agents_manager.router)
api_ninja.add_router("/tasks", router=task_manager_api.router)
api_ninja.add_router("", router=user_api.router)


api_ninja.add_router("", router=collection_mashine.router)
api_ninja.add_router("", router=collection_files.router)
api_ninja.add_router("", router=collection_password.router)
api_ninja.add_router("", router=collection_processe.router)


api_ninja.add_router("", router=execution_shell.router)

