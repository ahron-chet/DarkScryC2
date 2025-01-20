
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DarkScryC2Managment.settings")
django.setup()

from application.services.arq_tasks import remote_send_command_task
from arq.connections import RedisSettings

class WorkerSettings:
    # Which functions are our tasks?
    functions = [
        remote_send_command_task
    ]

    redis_settings = RedisSettings(
        host='127.0.0.1',
        port=6379,
        password='redissrv2025!',
        database=4
    )



