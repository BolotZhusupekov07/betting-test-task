from typing import Optional

from sqlalchemy import ColumnExpressionArgument
from src.common.repo import BaseRepo
from src.event.exceptions import EventNotFoundException
from src.event.model import EventDB
from src.event.schemas import Event, EventFilter


class EventRepo(BaseRepo):
    model = EventDB
    schema = Event
    not_found_exception_class = EventNotFoundException

    async def _get_list_where_args(
        self, filter_: Optional[EventFilter] = None
    ) -> list[ColumnExpressionArgument[bool]]:
        where_args: list[ColumnExpressionArgument[bool]] = [
            self.model.removed_at.is_(None)
        ]

        if not filter_:
            return where_args

        if filter_.guid:
            where_args.append(self.model.guid == filter_.guid)

        if filter_.state:
            where_args.append(self.model.state == filter_.state)

        if filter_.deadline__gt:
            where_args.append(self.model.deadline >= filter_.deadline__gt)

        return where_args
