import uuid
from unittest.mock import AsyncMock

import pytest

from src.bet.enums import BetStatusEnum
from src.bet.schemas import BetCreate, BetFilter, BetUpdate
from src.bet.service import BetService


@pytest.mark.asyncio
async def test_create_bet__success(bet_mock):
    repo = AsyncMock()
    event_api_repo = AsyncMock()
    settings = AsyncMock()

    service = BetService(
        repo=repo, event_api_repo=event_api_repo, settings=settings
    )

    event_api_repo.get_event.return_value = None
    repo.create.return_value = bet_mock

    bet_create = BetCreate(
        event_guid=uuid.uuid4(),
        amount=100,
    )
    result = await service.create(bet_create)

    assert result == bet_mock

    event_api_repo.get_event.assert_called_once()
    repo.create.assert_called_once_with(bet_create.model_dump())


@pytest.mark.asyncio
async def test_update_bets__success():
    repo = AsyncMock()
    event_api_repo = AsyncMock()
    settings = AsyncMock()

    service = BetService(
        repo=repo, event_api_repo=event_api_repo, settings=settings
    )

    repo.update.return_value = None

    bet_update = BetUpdate(status=BetStatusEnum.WON)
    bet_filter = BetFilter(event_guid=uuid.uuid4())
    await service.update(bet_filter, bet_update)

    repo.update.assert_called_once()


@pytest.mark.asyncio
async def test_find_all__success(bet_mock):
    repo = AsyncMock()
    service = BetService(repo)

    repo.find_all.return_value = [bet_mock]

    filter_ = BetFilter(guids=[uuid.uuid4()])

    result = await service.find_all(filter_)

    assert result == [bet_mock]

    repo.find_all.assert_called_once()
