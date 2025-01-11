import redis.asyncio as redis
from typing import Any, Optional

class RedisManager:
    def __init__(self, redis_url: str) -> None:
        """
        Initialize the AsyncRedisManager instance with a Redis connection URL.

        Args:
            redis_url (str): The URL of the Redis server (e.g., "redis://localhost:6379/0").
        """
        self.redis_url = redis_url
        self._connection: Optional[redis.Redis] = None

    async def connect(self) -> None:
        """
        Establish an asynchronous connection to the Redis server.
        """
        try:
            # Create an async Redis instance
            self._connection = redis.Redis.from_url(self.redis_url)
            
            # Test connection asynchronously
            await self._connection.ping()
        except redis.ConnectionError as e:
            raise RuntimeError(f"Failed to connect to Redis: {e}")

    async def set(
        self, 
        key: str, 
        value: Any, 
        expire: Optional[int] = None
    ) -> None:
        """
        Set a key-value pair in Redis with an optional expiration time.

        Args:
            key (str): The Redis key.
            value (Any): The value to store.
            expire (Optional[int]): Expiration time in seconds (default is None).
        """
        if not self._connection:
            raise RuntimeError("Redis connection is not established.")

        # Use await with the async Redis methods
        await self._connection.set(key, value, ex=expire)

    async def get(self, key: str) -> Optional[Any]:
        """
        Retrieve a value from Redis by key.

        Args:
            key (str): The Redis key.

        Returns:
            Optional[Any]: The value associated with the key, or None if not found.
        """
        if not self._connection:
            raise RuntimeError("Redis connection is not established.")

        value = await self._connection.get(key)
        return value.decode() if value else None

    async def delete(self, key: str) -> None:
        """
        Delete a key-value pair from Redis.

        Args:
            key (str): The Redis key to delete.
        """
        if not self._connection:
            raise RuntimeError("Redis connection is not established.")

        await self._connection.delete(key)

    async def close(self) -> None:
        """
        Close the connection to the Redis server.
        """
        if self._connection:
            # Close the underlying connection pool
            await self._connection.close()
            print("Redis connection closed.")

    async def exists(self, key: str) -> bool:
        """
        Check if a key exists in Redis.

        Args:
            key (str): The Redis key.

        Returns:
            bool: True if the key exists, False otherwise.
        """
        if not self._connection:
            raise RuntimeError("Redis connection is not established.")

        result = await self._connection.exists(key)
        return result > 0

    async def keys(self, pattern: str = "*") -> list[str]:
        """
        Retrieve a list of keys matching a pattern.

        Args:
            pattern (str): The pattern to match (default is "*").

        Returns:
            list[str]: A list of matching keys.
        """
        if not self._connection:
            raise RuntimeError("Redis connection is not established.")

        raw_keys = await self._connection.keys(pattern)
        return [key.decode() for key in raw_keys]

    async def flushdb(self) -> None:
        """
        Remove all keys from the current Redis database.
        """
        if not self._connection:
            raise RuntimeError("Redis connection is not established.")

        await self._connection.flushdb()
