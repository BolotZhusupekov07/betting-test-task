from fastapi import Depends
from redis.asyncio import Redis

from src.common.configs import Settings, get_settings


async def get_cache_client(
    settings: Settings = Depends(get_settings),
) -> Redis:
    return Redis(
        host=settings.redis.redis_host,
        port=settings.redis.redis_port,
        encoding="utf-8",
        decode_responses=True,
    )
