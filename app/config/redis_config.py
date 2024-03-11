import aioredis
from .base import settings

async def get_redis_pool():
    return aioredis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
