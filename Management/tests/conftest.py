import os
import sys

import pytest



# Ensure tests run exclusively against PostgreSQL
try:
    test_db_url = os.environ["TEST_DATABASE_URL"]
except KeyError as exc:
    raise RuntimeError("TEST_DATABASE_URL must be set for tests") from exc

os.environ.setdefault("MANAGEMENT_DATABASE_URL", test_db_url)
os.environ.setdefault("MANAGEMENT_SECRET_KEY", "secret")


@pytest.fixture()
def anyio_backend() -> str:
    """Force anyio to use the asyncio backend."""
    return "asyncio"
