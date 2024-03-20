from __future__ import annotations

from redis import asyncio

from .base import settings


async def get_redis_pool():
    return asyncio.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
