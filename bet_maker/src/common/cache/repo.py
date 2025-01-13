from typing import Any

from fastapi import Depends
from redis.asyncio import Redis

from src.common.cache.client import get_cache_client


class CacheRepo:
    def __init__(self, client: Redis = Depends(get_cache_client)) -> None:
        self._client = client

    async def get(self, key: str):
        return await self._client.get(key)

    async def set(self, key: str, value: Any, ex: None | int = None) -> None:
        await self._client.set(key, value, ex=ex)

    async def expire(self, key: str, time: int) -> None:
        await self._client.expire(key, time)

    async def delete(self, *key: str) -> None:
        await self._client.delete(*key)

    async def hset(self, hkey: str, field: str, value: Any, ttl: int) -> None:
        async with self._client.pipeline() as p:
            await p.hset(hkey, field, value).expire(hkey, ttl).execute()

    async def hget(self, hkey: str, field: str) -> Any:
        return await self._client.hget(hkey, field)

    async def hdelete(self, hkey: str, field: str) -> None:
        await self._client.hdel(hkey, field)

    async def setex(self, name, time, value) -> None:
        await self._client.setex(name, time, value)

    async def srandmember(self, key) -> Any:
        return await self._client.srandmember(key)

    async def llen(self, key: str) -> Any:
        return await self._client.llen(key)

    async def lrange(self, key: str, start: int, end: int) -> Any:
        return await self._client.lrange(key, start, end)

    async def rpush(self, key: str, value) -> Any:
        return await self._client.rpush(key, value)

    async def rpushx(self, key: str, value: str) -> Any:
        return await self._client.rpushx(key, value)

    async def scan_iter(self, key: str):
        data = self._client.scan_iter(key)
        async for d in data:
            yield d

    async def delete_by_key_prefix(self, prefix: str) -> None:
        async for key in self.scan_iter(f"{prefix}*"):
            await self.delete(key)
