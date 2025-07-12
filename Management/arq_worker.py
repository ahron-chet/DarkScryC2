from arq.connections import RedisSettings

from app.core.settings import get_arq_settings
from app.tasks import remote_send_command_task

settings = get_arq_settings()
print("🔧 ARQ Worker Settings Loaded:")
print(f"  - Redis Host: {settings.redis_host}")
print(f"  - Redis Port: {settings.redis_port}")
print(f"  - Redis Password: {'set' if settings.redis_password else 'not set'}")
print(f"  - Redis DB: {settings.arq_redis_db}")

class WorkerSettings:
    """Configuration for the ARQ worker."""

    functions = [remote_send_command_task]
    redis_settings = RedisSettings(
        host=settings.redis_host,
        port=settings.redis_port,
        password=settings.redis_password,
        database=settings.arq_redis_db
    )
