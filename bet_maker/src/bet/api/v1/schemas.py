from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from src.bet.enums import BetStatusEnum


class BetCreateIn(BaseModel):
    event_guid: UUID
    amount: Decimal = Field(decimal_places=2, gt=0)


class BetCreateOut(BaseModel):
    guid: UUID
    event_guid: UUID
    amount: Decimal
    status: BetStatusEnum

    created_at: datetime


class BetOut(BaseModel):
    guid: UUID
    event_guid: UUID
    amount: Decimal
    status: BetStatusEnum

    created_at: datetime
    updated_at: datetime
