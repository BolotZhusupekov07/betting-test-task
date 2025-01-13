from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from src.common.schemas import UpdateInBaseModel
from src.event.enums import EventStateEnum, EventStateUpdateInEnum


class EventCreateIn(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    coefficient: Decimal = Field(decimal_places=2, gt=0)
    deadline: int = Field(gt=0)


class EventUpdateIn(UpdateInBaseModel):
    state: EventStateUpdateInEnum


class EventCreateOut(BaseModel):
    guid: UUID
    title: str
    coefficient: Decimal
    deadline: int
    state: EventStateEnum

    created_at: datetime


class EventUpdateOut(BaseModel):
    guid: UUID
    title: str
    coefficient: Decimal
    deadline: int
    state: EventStateEnum

    updated_at: datetime


class EventOut(BaseModel):
    guid: UUID
    title: str
    coefficient: Decimal
    deadline: int
    state: EventStateEnum

    created_at: datetime
    updated_at: datetime
