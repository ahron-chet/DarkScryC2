import os
from typing import Optional

import redis.asyncio as redis

redis_pool: Optional[redis.Redis] = None


async def init_redis() -> None:
    url = os.getenv("MANAGEMENT_REDIS_URL")
    if not url:
        return
    global redis_pool
    redis_pool = redis.from_url(url)
    await redis_pool.ping()


async def close_redis() -> None:
    if redis_pool is not None:
        await redis_pool.close()
