import aioredis
import os


async def get_redis_pool():
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    return await aioredis.create_redis_pool(redis_url)
