from decimal import Decimal
from uuid import UUID

from sqlalchemy import Numeric
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import Mapped, mapped_column

from src.bet.enums import BetStatusEnum
from src.common.db.db_base_class import AuditableBase


class BetDB(AuditableBase):
    __tablename__ = "bet"

    event_guid: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True), nullable=False
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[BetStatusEnum] = mapped_column(
        ENUM(
            BetStatusEnum,
            name="bet_status_enum",
            create_type=False,
        ),
        nullable=False,
        default=BetStatusEnum.NEW,
        server_default=BetStatusEnum.NEW,
    )
