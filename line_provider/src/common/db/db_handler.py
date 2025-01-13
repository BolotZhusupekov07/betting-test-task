import logging
import re
from typing import Any, Optional, Type
from uuid import UUID

from fastapi import Depends
from sqlalchemy import Result, exc, exists, func, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql.dml import Insert, ReturningInsert

from src.common.db.db_base_class import AuditableDB
from src.common.db.db_session import get_db_engine, get_session_maker
from src.common.enums import DBIntegrityViolation
from src.common.exceptions import (
    DBIntegrityError,
    ObjectAlreadyExistsException,
    ObjectNotFoundException,
)

logger = logging.getLogger(__name__)


class Database:
    def __init__(
        self,
        engine: AsyncEngine = Depends(get_db_engine),
        session_maker: async_sessionmaker[AsyncSession] = Depends(
            get_session_maker
        ),
    ) -> None:
        self._engine = engine
        self._session_maker = session_maker

    @property
    def session_maker(self) -> async_sessionmaker[AsyncSession]:
        return self._session_maker

    async def execute_stmt(
        self,
        stmt,
        commit: bool = False,
        return_scalar: bool = False,
        session: Optional[AsyncSession] = None,
    ) -> Any:
        try:
            if return_scalar:
                return await self._execute_scalar(
                    stmt, commit=commit, session=session
                )

            return await self._execute(stmt, commit=commit, session=session)
        except exc.IntegrityError as error:
            await self._handle_integrity_error(error, session)

    async def insert_one(
        self,
        *,
        model: Type[AuditableDB],
        returning: Optional[Type[AuditableDB]] = None,
        commit: bool = False,
        session: Optional[AsyncSession] = None,
        **values,
    ) -> Any:
        stmt: Insert | ReturningInsert = insert(model).values(**values)

        if returning:
            stmt = stmt.returning(returning)

        return await self.execute_stmt(
            stmt=stmt,
            return_scalar=True if returning else False,
            commit=commit,
            session=session,
        )

    async def update_one(
        self,
        *,
        model: Type[AuditableDB],
        where: tuple,
        returning: Optional[Type[AuditableDB]] = None,
        commit: bool = False,
        session: Optional[AsyncSession] = None,
        **values,
    ) -> Any:
        stmt = update(model).where(*where).values(**values)
        if returning:
            stmt = stmt.returning(returning)

        return await self.execute_stmt(
            stmt=stmt,
            return_scalar=True if returning else False,
            commit=commit,
            session=session,
        )

    async def find_one_by_guid(
        self,
        *,
        model: Type[AuditableDB],
        guid_: UUID,
        session: Optional[AsyncSession] = None,
    ) -> Any:
        stmt = select(model).where(
            model.guid == guid_,
            model.removed_at.is_(None),
        )
        return await self.execute_stmt(
            stmt=stmt,
            return_scalar=True,
            commit=False,
            session=session,
        )

    async def find_one(
        self,
        *,
        model: Type[AuditableDB],
        where: tuple,
        session: Optional[AsyncSession] = None,
    ) -> Any:
        stmt = select(model).where(*where)
        return await self.execute_stmt(
            stmt=stmt,
            return_scalar=True,
            commit=False,
            session=session,
        )

    async def find_exists(
        self,
        *,
        model: Type[AuditableDB],
        where: tuple,
        session: Optional[AsyncSession] = None,
    ) -> bool:
        stmt = select(exists(select(model.guid).where(*where)))
        return await self.execute_stmt(
            stmt=stmt, return_scalar=True, session=session
        )

    async def count(
        self,
        *,
        model: Type[AuditableDB],
        where: tuple,
        session: Optional[AsyncSession] = None,
    ) -> int:
        stmt = select(func.count(model.guid)).where(*where)
        return await self.execute_stmt(
            stmt=stmt, return_scalar=True, session=session
        )

    async def create_all(self, base_class: Type[DeclarativeBase]):
        async with self._engine.begin() as conn:
            await conn.run_sync(base_class.metadata.create_all)

    async def drop_all(self, base_class: Type[DeclarativeBase]):
        async with self._engine.begin() as conn:
            await conn.run_sync(base_class.metadata.drop_all)

    async def _execute(
        self,
        stmt,
        commit: bool = False,
        session: Optional[AsyncSession] = None,
    ) -> Result:
        if session:
            result = await session.execute(stmt)
            if commit:
                await session.commit()
            return result
        else:
            async with self._session_maker() as s, s.begin():
                return await s.execute(stmt)

    async def _execute_scalar(
        self,
        stmt,
        commit: bool = False,
        session: Optional[AsyncSession] = None,
    ) -> Any:
        if session:
            result = await session.scalar(stmt)
            if commit:
                await session.commit()
            return result
        else:
            async with self._session_maker() as s, s.begin():
                return await s.scalar(stmt)

    async def _handle_foreign_key_violation(
        self, error: exc.IntegrityError
    ) -> None:
        pattern = r"Key \((.*?)_guid\)"
        match = re.search(pattern, str(error))

        if match:
            obj_title = match.group(1).capitalize()
            raise ObjectNotFoundException(obj_title)

    async def _handle_unique_index_violation(
        self, error: exc.IntegrityError
    ) -> None:
        field_title, unique_value, obj_title = None, None, None

        field_title_pattern = r"Key\s+\(([^)]+)\)=\(([^)]+)\)"
        field_title_match = re.search(field_title_pattern, str(error))

        unique_value_pattern = r"Key\s+\([^)]+\)=\(([^)]+)\)"
        unique_value_match = re.search(unique_value_pattern, str(error))

        obj_title_pattern = r"(?:INSERT INTO|UPDATE)\s+(\w+)\s+"
        obj_title_match = re.search(obj_title_pattern, str(error))

        if field_title_match and unique_value_match and obj_title_match:
            field_title = field_title_match.group(1)
            unique_value = unique_value_match.group(1)
            obj_title = obj_title_match.group(1).replace("_", " ").title()

        raise ObjectAlreadyExistsException(
            obj_title, field_title, unique_value
        )

    async def _handle_integrity_error(
        self, error: exc.IntegrityError, session: Optional[AsyncSession] = None
    ) -> None:
        if session:
            await session.rollback()

        logger.error(error)

        violation = error.orig.sqlstate  # type: ignore

        if violation == DBIntegrityViolation.FOREIGN_KEY:
            await self._handle_foreign_key_violation(error)

        elif violation == DBIntegrityViolation.UNIQUE:
            await self._handle_unique_index_violation(error)

        raise DBIntegrityError(message=str(error), violation=violation)
