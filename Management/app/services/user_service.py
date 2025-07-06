import uuid

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.security import (
    get_password_hash,
    validate_password_complexity,
    verify_password,
)
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate


class UserService:
    """Service object for user-related operations."""

    async def create(self, db: AsyncSession, user_in: UserCreate) -> User:
        """Create a new user after validating the password."""
        validate_password_complexity(user_in.password)
        user = User(
            username=user_in.username,
            password=get_password_hash(user_in.password),
            role=user_in.role.value,
        )
        db.add(user)
        try:
            await db.commit()
        except IntegrityError:
            await db.rollback()
            raise
        await db.refresh(user)
        return user

    async def authenticate(
        self, db: AsyncSession, username: str, password: str
    ) -> User | None:
        """Return the user if the credentials are valid."""
        result = await db.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()
        if user and user.is_active and verify_password(password, user.password):
            return user
        return None

    async def get(self, db: AsyncSession, user_id: uuid.UUID) -> User | None:
        """Retrieve a user by their public ID."""
        result = await db.execute(select(User).where(User.user_id == user_id))
        return result.scalar_one_or_none()

    async def list(self, db: AsyncSession) -> list[User]:
        """List all users by creation time."""
        result = await db.execute(select(User).order_by(User.time_generated.desc()))
        return list(result.scalars())

    async def update(self, db: AsyncSession, user: User, user_in: UserUpdate) -> User:
        """Update an existing user's attributes."""
        if user_in.username is not None:
            user.username = user_in.username
        if user_in.password is not None:
            validate_password_complexity(user_in.password)
            user.password = get_password_hash(user_in.password)
        if user_in.email is not None:
            user.email = user_in.email
        if user_in.role is not None:
            user.role = user_in.role.value
        if user_in.first_name is not None:
            user.first_name = user_in.first_name
        if user_in.last_name is not None:
            user.last_name = user_in.last_name
        if user_in.company_name is not None:
            user.company_name = user_in.company_name
        if user_in.industry is not None:
            user.industry = user_in.industry
        if user_in.country is not None:
            user.country = user_in.country
        if user_in.otpuri is not None:
            user.otpuri = user_in.otpuri
        await db.commit()
        await db.refresh(user)
        return user

    async def delete(self, db: AsyncSession, user: User) -> None:
        """Delete a user record."""
        await db.delete(user)
        await db.commit()
