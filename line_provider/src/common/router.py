from fastapi import APIRouter

from src.event.router import api_router as product_api_router

api_router = APIRouter()

api_router.include_router(product_api_router)