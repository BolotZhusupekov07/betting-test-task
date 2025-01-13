import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional
from unittest.mock import AsyncMock, Mock
from uuid import UUID

import pytest
from httpx import ASGITransport, AsyncClient

from main import app
from src.bet.enums import BetStatusEnum
from src.bet.model import BetDB
from src.bet.schemas import Bet
from src.common.configs import get_settings
from src.common.db.db_base_class import Base
from src.common.db.db_handler import Database
from src.common.db.db_session import get_db_engine, get_session_maker
from src.event.enums import EventStateEnum
from src.event.schemas import Event
from src.event.service import EventService


@pytest.fixture(scope="function")
async def database() -> Database:
    settings = await get_settings()
    engine = await get_db_engine(settings)
    session_maker = await get_session_maker(engine, settings)
    db = Database(engine=engine, session_maker=session_maker)
    await db.drop_all(Base)
    await db.create_all(Base)
    yield db
    await db.drop_all(Base)
    await db.create_all(Base)


@pytest.fixture(scope="function")
async def async_client() -> AsyncClient:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost/"
    ) as ac:
        yield ac

    app.dependency_overrides = {}


@pytest.fixture(scope="function")
async def bet(database: Database) -> BetDB:
    yield await database.insert_one(
        model=BetDB,
        returning=BetDB,
        event_guid=uuid.uuid4(),
        amount=10.22,
        status=BetStatusEnum.NEW,
    )


@pytest.fixture(scope="function")
async def bet_factory(database: Database) -> BetDB:
    async def _bet_factory(
        event_guid: Optional[UUID] = uuid.uuid4(),
        amount: Optional[Decimal] = 100,
        status: Optional[BetStatusEnum] = BetStatusEnum.NEW,
    ) -> BetDB:
        return await database.insert_one(
            model=BetDB,
            returning=BetDB,
            event_guid=event_guid,
            amount=amount,
            status=status,
        )

    yield _bet_factory


@pytest.fixture(scope="function")
async def bet_mock() -> BetDB:
    yield Bet(
        guid=uuid.uuid4(),
        event_guid=uuid.uuid4(),
        amount=100.22,
        status=BetStatusEnum.NEW,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


@pytest.fixture(scope="function")
async def event_mock() -> BetDB:
    yield Event(
        guid=uuid.uuid4(),
        title="title",
        coefficient=1.11,
        deadline=100,
        state=EventStateEnum.NEW,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


@pytest.fixture(scope="function")
async def event_service() -> EventService:
    yield EventService(
        event_api_repo=AsyncMock(),
        cache_repo=AsyncMock(),
        bet_service=AsyncMock(),
        settings=Mock(),
    )
