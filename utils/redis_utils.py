from config.redis_config import get_redis_pool


def get_redis():
    return get_redis_pool()
