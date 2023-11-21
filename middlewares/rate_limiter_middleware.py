from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi.responses import JSONResponse
import aioredis
import datetime
import os

MAX_REQUESTS = 10
TIME_WINDOW = 60


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        now = datetime.datetime.now()

        # Updated for aioredis v2.x
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        redis = aioredis.from_url(redis_url, encoding="utf-8", decode_responses=True)

        try:
            request_count = await redis.get(client_ip)
            request_count = int(request_count) if request_count else 0

            if request_count >= MAX_REQUESTS:
                ttl = await redis.ttl(client_ip)
                detail = {"error": "Too Many Requests", "message": f"Rate limit exceeded. Try again in {ttl} seconds."}
                return JSONResponse(status_code=429, content=detail)

            pipe = redis.pipeline()
            pipe.incr(client_ip)
            pipe.expire(client_ip, TIME_WINDOW)
            await pipe.execute()
        finally:
            pass

        response = await call_next(request)
        return response
