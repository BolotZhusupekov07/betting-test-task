from fastapi import APIRouter

from src.bet.router import api_router as bet_api_router
from src.event.router import api_router as event_api_router

api_router = APIRouter()

api_router.include_router(event_api_router)
api_router.include_router(bet_api_router)
