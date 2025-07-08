"""ARQ task utilities for scheduling background jobs."""

from __future__ import annotations

from arq import create_pool
from arq.connections import RedisSettings

from app.core.settings import get_settings

_redis_pool = None


async def get_task_executor():
    """Return a Redis connection pool for enqueueing jobs."""
    global _redis_pool
    if _redis_pool is None:
        settings = get_settings()
        _redis_pool = await create_pool(
            RedisSettings(
                host=settings.redis_host,
                port=settings.redis_port,
                password=settings.redis_password,
                database=settings.arq_redis_db,
            )
        )
    return _redis_pool


async def close_task_executors():
    global _redis_pool
    if _redis_pool is not None:
        await _redis_pool.close()
        _redis_pool = None
