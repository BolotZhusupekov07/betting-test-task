from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from src.event.api.v1.schemas import EventOut, EventStateWebhook
from src.event.service import EventService

router = APIRouter()


@router.get(
    "/api/v1/events/",
    status_code=status.HTTP_200_OK,
    summary="Get events",
    response_model=list[EventOut],
)
async def get_events(service: EventService = Depends()):
    return await service.get_events()


@router.post(
    "/api/v1/events/{guid}/state/webhook/",
    status_code=status.HTTP_200_OK,
    summary="Update event state webhook",
)
async def event_state_webhook(
    guid: UUID, schema: EventStateWebhook, service: EventService = Depends()
):
    await service.handle_event_state_webhook(guid, schema)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
