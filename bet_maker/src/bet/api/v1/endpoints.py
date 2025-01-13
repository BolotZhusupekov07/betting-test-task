from fastapi import APIRouter, Depends, status

from src.bet.api.v1.schemas import BetCreateIn, BetCreateOut, BetOut
from src.bet.schemas import BetCreate
from src.bet.service import BetService

router = APIRouter()


@router.post(
    "/api/v1/bets/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a bet",
    response_model=BetCreateOut,
)
async def create(schema_in: BetCreateIn, service: BetService = Depends()):
    schema = BetCreate(**schema_in.model_dump())
    return await service.create(schema)


@router.get(
    "/api/v1/bets/",
    status_code=status.HTTP_200_OK,
    summary="Get bets",
    response_model=list[BetOut],
)
async def get_bets(service: BetService = Depends()):
    return await service.find_all()
