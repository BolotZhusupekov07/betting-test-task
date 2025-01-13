from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from src.event.enums import EventStateEnum, EventStateEnumWebhook


class EventOut(BaseModel):
    guid: UUID
    title: str
    coefficient: Decimal
    deadline: int
    state: EventStateEnum

    created_at: datetime
    updated_at: datetime


class EventStateWebhook(BaseModel):
    state: EventStateEnumWebhook
