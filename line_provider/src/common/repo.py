from datetime import datetime, timezone
from typing import Any, Optional, Type
from uuid import UUID

from fastapi import Depends
from pydantic import BaseModel, TypeAdapter
from sqlalchemy import ColumnExpressionArgument, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.db.db_base_class import AuditableBase
from src.common.db.db_handler import Database
from src.common.exceptions import ObjectNotFoundException


class BaseRepo:
    model: Type[AuditableBase]
    schema: Type[BaseModel]
    not_found_exception_class: Type[ObjectNotFoundException]

    def __init__(self, db: Database = Depends()) -> None:
        self.db = db

    async def delete(
        self,
        guid: UUID,
        session: Optional[AsyncSession] = None,
    ) -> None:
        await self.db.update_one(
            model=self.model,
            where=(self.model.guid == guid,),
            returning=self.model,
            commit=True,
            session=session,
            removed_at=datetime.now(tz=timezone.utc),
        )

    async def create(
        self,
        data: dict[Any, Any],
        session: Optional[AsyncSession] = None,
    ) -> Any:
        obj_db = await self.db.insert_one(
            model=self.model,
            returning=self.model,
            commit=True,
            session=session,
            **data,
        )

        return self.schema.model_validate(obj_db)

    async def update(
        self,
        guid: UUID,
        data: dict[Any, Any],
        session: Optional[AsyncSession] = None,
    ) -> None:
        await self.db.update_one(
            model=self.model,
            where=(self.model.guid == guid,),
            returning=self.model,
            commit=True,
            session=session,
            **data,
        )

    async def find_one_by_guid(
        self, guid: UUID, session: Optional[AsyncSession] = None
    ) -> Any | None:
        obj_db = await self.db.find_one_by_guid(
            model=self.model, guid_=guid, session=session
        )
        return self.schema.model_validate(obj_db) if obj_db else None

    async def find_one_or_raise(
        self, filter_: Any, session: Optional[AsyncSession] = None
    ) -> Any:
        where_args = await self._get_list_where_args(filter_)
        obj_db = await self.db.find_one(
            model=self.model,
            where=where_args,
            session=session
        )
        if not obj_db:
            raise self.not_found_exception_class()

        return self.schema.model_validate(obj_db)

    async def find_one_by_guid_or_raise(
        self, guid: UUID, session: Optional[AsyncSession] = None
    ) -> Any:
        obj = await self.find_one_by_guid(guid, session)
        if not obj:
            raise self.not_found_exception_class()

        return obj

    async def find_all(
        self,
        filter_: Optional[Any] = None,
        session: Optional[AsyncSession] = None,
    ) -> list[Any]:
        where_args = await self._get_list_where_args(filter_)

        list_stmt = (
            select(self.model)
            .where(*where_args)
            .distinct(self.model.guid)
            .order_by(self.model.guid.desc())
        )
        list_db = await self.db.execute_stmt(
            stmt=list_stmt, return_scalar=False, commit=False, session=session
        )
        list_schema = TypeAdapter(list[self.schema]).validate_python(  # type: ignore
            list_db.scalars().all()
        )

        return list_schema

    async def _get_list_where_args(
        self, filter_: Optional[Any] = None
    ) -> list[ColumnExpressionArgument[bool]]:
        where_args: list[ColumnExpressionArgument[bool]] = [
            self.model.removed_at.is_(None)
        ]

        if not filter_:
            return where_args

        return where_args
