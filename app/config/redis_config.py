from .base import settings
from redis import asyncio

async def get_redis_pool():
    return asyncio.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
