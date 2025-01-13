import time
from uuid import UUID

from fastapi import Depends
import httpx

from src.event.repos import EventRepo
from src.event.schemas import (
    Event,
    EventCreate,
    EventFilter,
    EventUpdate,
)
from src.event.enums import EventStateEnum
from src.event.exceptions import EventInvalidException
from src.common.configs import Settings, get_settings


class EventService:
    def __init__(
        self,
        repo: EventRepo = Depends(),
        settings: Settings = Depends(get_settings)
    ):
        self._repo = repo
        self._settings = settings

    async def create(self, schema: EventCreate) -> Event:
        if schema.deadline < int(time.time()):
            raise EventInvalidException('Deadline is invalid!')

        return await self._repo.create(schema.model_dump())

    async def update(self, guid: UUID, schema: EventUpdate) -> Event:
        await self._repo.find_one_or_raise(
            EventFilter(
                state=EventStateEnum.NEW,
                deadline__gt=int(time.time())
            )
        )
        await self._repo.update(
            guid, schema.model_dump(exclude_unset=True, exclude_none=True)
        )
        event = await self._repo.find_one_by_guid_or_raise(guid)

        await self._webhook_to_bet_maker(event)

        return event

    async def _webhook_to_bet_maker(self, event: Event) -> None:
        url = (
            f'{self._settings.bet_maker_service_domain}'
            f'/api/v1/events/{event.guid}/state/webhook/'
        )
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url=url,
                json={'state': event.state}
            )
            return response

    async def find_one_or_raise(self, guid: UUID) -> Event:
        return await self._repo.find_one_or_raise(
            EventFilter(
                guid=guid,
                state=EventStateEnum.NEW,
                deadline__gt=int(time.time())
            )
        )

    async def find_all(self) -> list[Event]:
        filter_ = EventFilter(
            state=EventStateEnum.NEW,
            deadline__gt=int(time.time())
        )
        return await self._repo.find_all(filter_)
