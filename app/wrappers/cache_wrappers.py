from redis import asyncio
from dotenv import load_dotenv

from app.config.base import settings

if not settings.REDIS_URL:
    raise Exception("Please add REDIS_URL in environment")

redis = asyncio.from_url(settings.REDIS_URL)


async def create_cache(resp, key: str, ex: int = 60):
    await redis.set(key, resp, ex=ex)


async def retrieve_cache(key: str):
    data = await redis.get(key)
    if not data:
        return None
    expire = await redis.ttl(key)
    return data, expire


async def invalidate_cache(key: str):
    await redis.delete(key)