import redis
import os


def get_redis_pool():
    return redis.Redis(host="localhost", port=6379, db=0)
