from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.event.api.v1.schemas import (
    EventCreateIn,
    EventCreateOut,
    EventOut,
    EventUpdateIn,
    EventUpdateOut,
)
from src.event.schemas import (
    EventCreate,
    EventUpdate,
)
from src.event.service import EventService

router = APIRouter()


@router.post(
    "/api/v1/events/",
    status_code=status.HTTP_201_CREATED,
    summary="Create an event",
    response_model=EventCreateOut,
)
async def create(
    schema_in: EventCreateIn, service: EventService = Depends()
):
    schema = EventCreate(**schema_in.model_dump())
    return await service.create(schema)


@router.patch(
    "/api/v1/events/{guid}/",
    status_code=status.HTTP_200_OK,
    summary="Update an event state",
    response_model=EventUpdateOut,
)
async def update(
    guid: UUID, schema_in: EventUpdateIn, service: EventService = Depends()
):
    schema = EventUpdate(**schema_in.model_dump())
    return await service.update(guid, schema)


@router.get(
    "/api/v1/events/{guid}/",
    status_code=status.HTTP_200_OK,
    summary="Get an active event detail",
    response_model=EventOut,
)
async def get_event(guid: UUID, service: EventService = Depends()):
    return await service.find_one_or_raise(guid)


@router.get(
    "/api/v1/events/",
    status_code=status.HTTP_200_OK,
    summary="Get events",
    response_model=list[EventOut],
)
async def get_events(service: EventService = Depends()):
    return await service.find_all()