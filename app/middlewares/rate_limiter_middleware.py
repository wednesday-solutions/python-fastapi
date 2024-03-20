from __future__ import annotations

from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.config.redis_config import get_redis_pool

MAX_REQUESTS = 10000
TIME_WINDOW = 60


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host

        redis = await get_redis_pool()
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
            print("Finally Block in Rate Limit exceeded")

        response = await call_next(request)
        return response
