import uuid

from sqlalchemy import DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from .base import Base


class Agent(Base):
    __tablename__ = "application_agent"

    agent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
    )
    host_name: Mapped[str] = mapped_column(String(255))
    os: Mapped[str] = mapped_column(String(100))
    last_time_update: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    onboarded_time: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    def __repr__(self) -> str:
        return f"<Agent {self.host_name}>"
