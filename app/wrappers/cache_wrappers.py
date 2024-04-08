from __future__ import annotations

from app.config.redis_config import get_redis_pool


class CacheUtils:
    @classmethod
    async def create_cache(cls, resp, key: str, ex: int = 60):
        redis = await get_redis_pool()
        await redis.set(key, resp, ex=ex)

    @classmethod
    async def retrieve_cache(cls, key: str):
        redis = await get_redis_pool()
        data = await redis.get(key)
        if not data:
            return None, None
        expire = await redis.ttl(key)
        return data, expire

    @classmethod
    async def invalidate_cache(cls, key: str):
        redis = await get_redis_pool()
        await redis.delete(key)
