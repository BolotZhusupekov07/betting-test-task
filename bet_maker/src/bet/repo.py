from sqlalchemy import ColumnExpressionArgument, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.bet.exceptions import BetNotFoundException
from src.bet.model import BetDB
from src.bet.schemas import Bet, BetFilter, BetUpdate
from src.common.repo import BaseRepo


class BetRepo(BaseRepo):
    model = BetDB
    schema = Bet
    not_found_exception_class = BetNotFoundException

    async def update(
        self,
        filter_: BetFilter,
        schema: BetUpdate,
        session: AsyncSession | None = None,
    ) -> None:
        where_args = await self._get_list_where_args(filter_)
        stmt = (
            update(self.model).where(*where_args).values(**schema.model_dump())
        )
        return await self.db.execute_stmt(
            stmt=stmt,
            commit=True,
            session=session,
        )

    async def _get_list_where_args(
        self, filter_: BetFilter | None = None
    ) -> list[ColumnExpressionArgument[bool]]:
        where_args: list[ColumnExpressionArgument[bool]] = [
            self.model.removed_at.is_(None)
        ]
        if not filter_:
            return where_args

        if filter_.guids:
            where_args.append(self.model.guid.in_(filter_.guids))

        if filter_.event_guid:
            where_args.append(self.model.event_guid == filter_.event_guid)

        if filter_.status:
            where_args.append(self.model.status == filter_.status)

        return where_args
