import json
from uuid import UUID

from fastapi import Depends

from src.bet.enums import BetStatusEnum, BetStatusUpdateEnum
from src.bet.schemas import BetFilter, BetUpdate
from src.bet.service import BetService
from src.common.cache.repo import CacheRepo
from src.common.configs import Settings, get_settings
from src.event.constants import EVENTS_CACHE_KEY, EVENTS_EXPIRATION_SECONDS
from src.event.enums import EventStateEnum
from src.event.repo import EventAPIRepo
from src.event.schemas import Event, EventStateWebhook


class EventService:
    def __init__(
        self,
        event_api_repo: EventAPIRepo = Depends(),
        cache_repo: CacheRepo = Depends(),
        bet_service: BetService = Depends(),
        settings: Settings = Depends(get_settings),
    ):
        self._event_api_repo = event_api_repo
        self._bet_service = bet_service
        self._cache_repo = cache_repo
        self._settings = settings

    async def get_events(self) -> list[Event]:
        events_from_cache = await self._get_events_from_cache()
        if events_from_cache:
            return events_from_cache

        events = await self._event_api_repo.get_events(
            service_domain=self._settings.event_service_domain
        )
        await self._cache_repo.set(
            EVENTS_CACHE_KEY,
            json.dumps([event.model_dump_json() for event in events]),
            EVENTS_EXPIRATION_SECONDS,
        )
        return events

    async def _get_events_from_cache(self) -> list[Event] | None:
        events = await self._cache_repo.get(EVENTS_CACHE_KEY)
        if events:
            return [Event(**json.loads(event)) for event in json.loads(events)]

    async def handle_event_state_webhook(
        self, event_guid: UUID, schema: EventStateWebhook
    ) -> None:
        bets = await self._bet_service.find_all(
            BetFilter(event_guid=event_guid, status=BetStatusEnum.NEW)
        )
        await self._bet_service.update(
            BetFilter(guids=[bet.guid for bet in bets]),
            BetUpdate(
                status=(
                    BetStatusUpdateEnum.WON
                    if schema.state == EventStateEnum.FINISHED_WIN
                    else BetStatusUpdateEnum.LOST
                )
            ),
        )
