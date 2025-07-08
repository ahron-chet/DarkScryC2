from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserCreate, UserRole
from app.services.user_service import UserService


async def create_user(
    db: AsyncSession,
    username: str,
    password: str = "Str0ng!Pass",
    role: UserRole = UserRole.ADMIN,
    email: str | None = None,
):
    """Create a user in the database for testing."""
    service = UserService()
    return await service.create(
        db,
        UserCreate(
            username=username,
            password=password,
            email=email or f"{username}@example.com",
            role=role,
        ),
    )


async def login(client: AsyncClient, username: str, password: str) -> str:
    """Return an access token for the given credentials."""
    resp = await client.post(
        "/auth/login", json={"username": username, "password": password}
    )
    return resp.json()["access_token"]
