import logging
from typing import Any
from uuid import UUID

import httpx
from httpx import Response

from src.event.exceptions import EventAPIException, EventNotFoundException
from src.event.schemas import Event

logger = logging.getLogger(__name__)


class EventAPIRepo:
    async def _request(
        self,
        url: str,
        method: str = "POST",
        json: Any = None,
    ) -> Response:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(
                    method=method, url=url, json=json
                )
                return response
        except httpx.RequestError as error:
            logger.error(error)
            raise EventAPIException()

    async def get_events(self, service_domain: str) -> list[Event]:
        url = f"{service_domain}/api/v1/events/"
        print(url)
        response = await self._request(url, method="GET")
        if response.status_code == 200:
            response_data = response.json()
            return [Event(**event) for event in response_data]

        raise EventAPIException()

    async def get_event(self, service_domain: str, guid: UUID) -> Event:
        url = f"{service_domain}/api/v1/events/{guid}/"
        response = await self._request(url, method="GET")
        if response.status_code == 200:
            response_data = response.json()
            return Event(**response_data)
        elif response.status_code == 404:
            raise EventNotFoundException()

        raise EventAPIException()
