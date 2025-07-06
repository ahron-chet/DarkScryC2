import os

os.environ.setdefault(
    "MANAGEMENT_DATABASE_URL",
    os.getenv("TEST_DATABASE_URL", "postgresql+asyncpg://user:pass@localhost/db"),
)
os.environ.setdefault("MANAGEMENT_SECRET_KEY", "secret")

from Management.app.models.agent import Agent
from Management.app.models.user import User


def test_models_have_tables():
    assert User.__tablename__ == "user"
    assert Agent.__tablename__ == "application_agent"
