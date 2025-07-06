import uuid

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from .base import Base


class Agent(Base):
    __tablename__ = "application_agent"

    AgentId: Mapped[uuid.UUID] = mapped_column(
        "AgentId",
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
    )
    HostName: Mapped[str] = mapped_column(String(255))
    Os: Mapped[str] = mapped_column(String(100))
    LastTimeUpdate: Mapped[DateTime] = mapped_column(
        DateTime, server_default=func.now()
    )
    OnboardedTime: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    def __repr__(self) -> str:
        return f"<Agent {self.HostName}>"
