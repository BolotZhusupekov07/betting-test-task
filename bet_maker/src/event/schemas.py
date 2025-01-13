from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.event.enums import EventStateEnum, EventStateEnumWebhook


class Event(BaseModel):
    guid: UUID

    title: str
    coefficient: Decimal
    deadline: int
    state: EventStateEnum

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class EventStateWebhook(BaseModel):
    state: EventStateEnumWebhook
