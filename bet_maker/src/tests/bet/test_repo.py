import uuid

import pytest

from src.bet.enums import BetStatusEnum, BetStatusUpdateEnum
from src.bet.repo import BetRepo
from src.bet.schemas import BetCreate, BetFilter, BetUpdate


@pytest.mark.asyncio
async def test_find_all__returns_valid_bets__with_right_filters(
    database, bet_factory
):
    event_1_guid = uuid.uuid4()
    event_2_guid = uuid.uuid4()

    bet_1 = await bet_factory(
        event_guid=event_1_guid, amount=100, status=BetStatusEnum.NEW
    )
    await bet_factory(event_guid=event_2_guid)

    repo = BetRepo(database)

    bets = await repo.find_all(BetFilter(event_guid=event_1_guid))

    assert bets[0].guid == bet_1.guid


@pytest.mark.asyncio
async def test_find_all__returns_all_bets__with_no_filters(
    database, bet_factory
):
    await bet_factory()
    await bet_factory()

    repo = BetRepo(database)

    result = await repo.find_all()

    assert len(result) == 2


@pytest.mark.asyncio
async def test_find_all__returns_valid_bets__with_wrong_filters(
    database, bet_factory
):
    event_1_guid = uuid.uuid4()
    event_2_guid = uuid.uuid4()

    bet_1 = await bet_factory(
        event_guid=event_1_guid, amount=100, status=BetStatusEnum.NEW
    )
    await bet_factory(event_guid=event_2_guid)

    repo = BetRepo(database)

    bets = await repo.find_all(BetFilter(event_guid=uuid.uuid4()))

    assert len(bets) == 0


@pytest.mark.asyncio
async def test_create__success(database):
    repo = BetRepo(database)

    schema = BetCreate(event_guid=uuid.uuid4(), amount=100)
    result = await repo.create(schema.model_dump())

    assert result.event_guid == schema.event_guid
    assert result.amount == schema.amount


@pytest.mark.asyncio
async def test_update__success(database, bet):
    repo = BetRepo(database)

    await repo.update(
        BetFilter(guids=[bet.guid], event_guid=bet.event_guid),
        BetUpdate(status=BetStatusUpdateEnum.WON),
    )

    result = await repo.find_one_by_guid(bet.guid)

    assert result.status == BetStatusEnum.WON


@pytest.mark.asyncio
async def test_update__success__with_session(database, bet):
    repo = BetRepo(database)

    async with repo.db._session_maker() as session, session.begin():
        await repo.update(
            BetFilter(guids=[bet.guid], event_guid=bet.event_guid),
            BetUpdate(status=BetStatusUpdateEnum.WON),
            session=session,
        )

    result = await repo.find_one_by_guid(bet.guid)

    assert result.status == BetStatusEnum.WON


@pytest.mark.asyncio
async def test_find_one_by_guid_or_raise__success(database, bet):
    repo = BetRepo(database)

    result = await repo.find_one_by_guid_or_raise(bet.guid)

    assert result.guid == bet.guid
