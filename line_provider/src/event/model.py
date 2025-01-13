from decimal import Decimal

from sqlalchemy import Integer, Numeric
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column

from src.common.db.db_base_class import AuditableBase
from src.event.enums import EventStateEnum
from src.common.db.db_type import (
    title_non_nullable,
)


class EventDB(AuditableBase):
    __tablename__ = "event"

    title: Mapped[title_non_nullable]
    coefficient: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False
    )
    deadline: Mapped[int] = mapped_column(Integer, nullable=False)
    state: Mapped[EventStateEnum] = mapped_column(
        ENUM(
            EventStateEnum,
            name="event_state_enum",
            create_type=False,
        ),
        nullable=False,
        default=EventStateEnum.NEW,
        server_default=EventStateEnum.NEW,
    )
