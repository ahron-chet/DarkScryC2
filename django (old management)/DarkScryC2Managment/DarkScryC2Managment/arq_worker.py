
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DarkScryC2Managment.settings")
django.setup()

from application.services.arq_tasks import remote_send_command_task, remote_send_web_cred_gather
from arq.connections import RedisSettings
from darkscryc2server.Utils import getenv_nonempty

class WorkerSettings:
    functions = [
        remote_send_command_task,
        remote_send_web_cred_gather
    ]

    redis_settings = RedisSettings(
        host=getenv_nonempty("REDIS_HOST", "redis"),
        port=int(getenv_nonempty("REDIS_PORT", "6379")),
        password=getenv_nonempty("REDIS_PASSWORD", None),
        database=int(getenv_nonempty("ARQ_REDIS_DB", "4"))
    )



