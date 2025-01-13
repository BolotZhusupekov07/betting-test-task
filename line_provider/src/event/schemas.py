from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.event.enums import EventStateEnum


class Event(BaseModel):
    guid: UUID

    title: str
    coefficient: Decimal
    deadline: int
    state: EventStateEnum

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class EventCreate(BaseModel):
    title: str
    coefficient: Decimal
    deadline: int


class EventUpdate(BaseModel):
    title: Optional[str] = None
    coefficient: Optional[Decimal] = None
    deadline: Optional[int] = None
    state: Optional[EventStateEnum] = None


class EventFilter(BaseModel):
    guid: Optional[UUID] = None
    deadline__gt: Optional[int] = None
    state: Optional[EventStateEnum] = None