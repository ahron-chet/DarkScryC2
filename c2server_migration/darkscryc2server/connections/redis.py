
from redis.asyncio import Redis

class RedisClient:
    """Thin wrapper around redis.asyncio for easy mocking."""

    def __init__(self, url: str) -> None:
        self.url = url
        self._redis: Redis | None = None

    async def connect(self) -> None:
        self._redis = Redis.from_url(self.url)
        await self._redis.ping()

    async def set(self, key: str, value: bytes) -> None:
        if self._redis is None:
            raise RuntimeError("Redis not connected")
        await self._redis.set(key, value)

    async def get(self, key: str) -> bytes | None:
        if self._redis is None:
            raise RuntimeError("Redis not connected")
        return await self._redis.get(key)

    async def delete(self, key: str) -> None:
        if self._redis is None:
            raise RuntimeError("Redis not connected")
        await self._redis.delete(key)

    async def close(self) -> None:
        if self._redis:
            await self._redis.close()
            self._redis = None
