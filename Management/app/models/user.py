import uuid
from enum import Enum

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class UserRole(str, Enum):
    """Available user roles."""

    READER = "reader"
    OPERATOR = "operator"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(150), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    last_login = Column(DateTime(timezone=True), nullable=True)
    is_superuser = Column(Boolean, default=False)
    first_name = Column(String(150), nullable=True)
    last_name = Column(String(150), nullable=True)
    email = Column(String(254), nullable=True)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    date_joined = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    user_id = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4)
    role = Column(String(20), default=UserRole.READER.value, nullable=False)
    otpuri = Column(Text, nullable=True)
    company_name = Column(String(100), nullable=True)
    industry = Column(String(100), nullable=True)
    country = Column(String(50), nullable=True)
    time_generated = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    # relationships placeholder

    def __repr__(self) -> str:
        return f"<User username={self.username} role={self.role}>"
