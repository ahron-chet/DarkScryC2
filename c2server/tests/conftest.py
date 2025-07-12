import os
import sys
import warnings

import pytest

warnings.filterwarnings(
    "ignore", "Passing 'msg' argument to.*cancel", DeprecationWarning
)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

os.environ.setdefault("C2_SERVER_HOST", "127.0.0.1")
os.environ.setdefault("C2_SERVER_PORT", "9100")
os.environ.setdefault("C2_SERVER_REDIS_URL", "redis://localhost")


class FakeRedisClient:
    def __init__(self) -> None:
        self.store: dict[str, bytes] = {}

    async def connect(self) -> None:  # pragma: no cover - no-op
        pass

    async def set(self, key: str, value: bytes) -> None:
        self.store[key] = value

    async def get(self, key: str) -> bytes | None:
        return self.store.get(key)

    async def delete(self, key: str) -> None:
        self.store.pop(key, None)

    async def close(self) -> None:  # pragma: no cover - no-op
        pass


@pytest.fixture()
def fake_redis(monkeypatch: pytest.MonkeyPatch) -> FakeRedisClient:
    fake = FakeRedisClient()
    monkeypatch.setattr(
        "darkscryc2server.core.connection.RedisClient", lambda url: fake
    )
    return fake
