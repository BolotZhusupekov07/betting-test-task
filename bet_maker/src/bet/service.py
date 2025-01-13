from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.bet.repo import BetRepo
from src.bet.schemas import Bet, BetCreate, BetFilter, BetUpdate
from src.common.configs import Settings, get_settings
from src.event.repo import EventAPIRepo


class BetService:
    def __init__(
        self,
        repo: BetRepo = Depends(),
        event_api_repo: EventAPIRepo = Depends(),
        settings: Settings = Depends(get_settings),
    ):
        self._repo = repo
        self._event_api_repo = event_api_repo
        self._settings = settings

    async def create(self, schema: BetCreate) -> Bet:
        await self._event_api_repo.get_event(
            service_domain=self._settings.event_service_domain,
            guid=schema.event_guid,
        )
        return await self._repo.create(schema.model_dump())

    async def update(
        self,
        filter_: BetFilter,
        schema: BetUpdate,
        session: AsyncSession | None = None,
    ) -> None:
        await self._repo.update(filter_, schema, session)

    async def find_all(self, filter_: BetFilter | None = None) -> list[Bet]:
        return await self._repo.find_all(filter_)
