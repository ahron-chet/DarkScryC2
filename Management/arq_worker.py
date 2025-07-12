from arq.connections import RedisSettings

from app.core.settings import get_arq_settings
from app.tasks import remote_send_command_task

settings = get_arq_settings()


class WorkerSettings:
    """Configuration for the ARQ worker."""

    functions = [remote_send_command_task]
    redis_settings = RedisSettings(
        host=settings.redis_host,
        port=settings.redis_port,
        password=settings.redis_password,
        database=settings.arq_redis_db
    )
