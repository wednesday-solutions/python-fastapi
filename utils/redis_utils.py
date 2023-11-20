from config.redis_config import get_redis_pool


async def get_redis():
    return await get_redis_pool()
