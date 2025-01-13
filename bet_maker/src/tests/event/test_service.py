import uuid
from unittest.mock import AsyncMock

import pytest

from src.event.api.v1.schemas import EventStateWebhook
from src.event.enums import EventStateEnumWebhook


@pytest.mark.asyncio
async def test_get_events_from_api(event_service, event_mock):
    event_service._get_events_from_cache = AsyncMock(return_value=None)
    event_service._event_api_repo.get_events.return_value = [event_mock]
    event_service._cache_repo.set.return_value = None
    result = await event_service.get_events()

    assert result == [event_mock]

    event_service._get_events_from_cache.assert_called_once_with()
    event_service._event_api_repo.get_events.assert_called_once()
    event_service._cache_repo.set.assert_called_once()


@pytest.mark.asyncio
async def test_get_events_from_cache(event_service, event_mock):
    event_service._get_events_from_cache = AsyncMock(return_value=[event_mock])
    result = await event_service.get_events()

    assert result == [event_mock]

    event_service._get_events_from_cache.assert_called_once_with()
    event_service._event_api_repo.get_events.assert_not_called()
    event_service._cache_repo.set.assert_not_called()


@pytest.mark.asyncio
async def test_handle_event_state_webhook(event_service, bet_mock):
    event_service._bet_service.find_all.return_value = [bet_mock]
    event_service._bet_service.update.return_value = None

    schema = EventStateWebhook(state=EventStateEnumWebhook.FINISHED_WIN)
    await event_service.handle_event_state_webhook(uuid.uuid4(), schema)

    event_service._bet_service.find_all.assert_called_once()
    event_service._bet_service.update.assert_called_once()
