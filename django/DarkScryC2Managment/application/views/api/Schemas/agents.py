from ninja import Schema
from uuid import UUID
from datetime import datetime

class AgentIn(Schema):
    HostName: str
    Os: str

class AgentOut(Schema):
    AgentId: UUID
    HostName: str
    Os: str
    LastTimeUpdate: datetime
    OnboardedTime: datetime
    is_active: bool
    address: str