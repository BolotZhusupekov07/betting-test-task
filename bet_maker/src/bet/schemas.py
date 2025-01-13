from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.bet.enums import BetStatusEnum, BetStatusUpdateEnum


class Bet(BaseModel):
    guid: UUID

    event_guid: UUID
    amount: Decimal
    status: BetStatusEnum

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BetCreate(BaseModel):
    event_guid: UUID
    amount: Decimal


class BetUpdate(BaseModel):
    status: BetStatusUpdateEnum


class BetFilter(BaseModel):
    guids: Optional[list[UUID]] = None
    event_guid: Optional[UUID] = None
    status: Optional[BetStatusEnum] = None
