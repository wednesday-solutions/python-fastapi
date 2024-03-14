from __future__ import annotations

from app.config.base import settings
from app.config.redis_config import get_redis_pool
from app.exceptions import RedisUrlNotFoundException

if not settings.REDIS_URL:
    raise RedisUrlNotFoundException("Failed To get Redis URL")


async def create_cache(resp, key: str, ex: int = 60):
    redis = await get_redis_pool()
    await redis.set(key, resp, ex=ex)


async def retrieve_cache(key: str):
    redis = await get_redis_pool()
    data = await redis.get(key)
    if not data:
        return None, None
    expire = await redis.ttl(key)
    return data, expire


async def invalidate_cache(key: str):
    redis = await get_redis_pool()
    await redis.delete(key)
