import re
import uuid
from datetime import UTC, datetime, timedelta
from typing import Callable, Optional

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.user import User, UserRole
from .database import get_db
from .settings import get_app_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

_password_complexity_regex = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$"
)


def validate_password_complexity(password: str) -> None:
    """Raise ValueError if the password is not complex enough."""
    if not _password_complexity_regex.match(password):
        raise ValueError("Password does not meet strength requirements")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    settings = get_app_settings()
    to_encode = data.copy()
    now = datetime.now(UTC)
    expire = now + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode.update(
        {
            "exp": expire,
            "iat": now,
            "iss": settings.jwt_issuer,
            "aud": settings.jwt_audience,
            "jti": str(uuid.uuid4()),
        }
    )
    return jwt.encode(to_encode, settings.secret_key, algorithm="HS256")


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    settings = get_app_settings()
    to_encode = data.copy()
    now = datetime.now(UTC)
    expire = now + (expires_delta or timedelta(days=settings.refresh_token_expire_days))
    to_encode.update(
        {
            "exp": expire,
            "iat": now,
            "iss": settings.jwt_issuer,
            "aud": settings.jwt_audience,
            "jti": str(uuid.uuid4()),
        }
    )
    return jwt.encode(to_encode, settings.secret_key, algorithm="HS256")


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    settings = get_app_settings()
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=["HS256"],
            issuer=settings.jwt_issuer,
            audience=settings.jwt_audience,
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise JWTError()
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    result = await db.execute(select(User).where(User.user_id == uuid.UUID(user_id)))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")
    return user


def required_role(role: UserRole) -> Callable[[User], User]:
    """Return dependency ensuring the current user has the given role."""

    async def _checker(user: User = Depends(get_current_user)) -> User:
        if user.role != role.value and user.role != UserRole.ADMIN.value:
            raise HTTPException(status_code=403, detail="Not authorized")
        return user

    return _checker
