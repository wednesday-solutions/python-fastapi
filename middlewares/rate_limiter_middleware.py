from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi.responses import JSONResponse
import datetime
from utils import redis_utils

MAX_REQUESTS = 10
TIME_WINDOW = 60


class RateLimitMiddleware(BaseHTTPMiddleware):
    def dispatch(self, request: Request, call_next):
        try:
            client_ip = request.client.host
            now = datetime.datetime.now()

            redis = redis_utils.get_redis()

            request_count = redis.get(client_ip)
            request_count = int(request_count) if request_count else 0

            if request_count >= MAX_REQUESTS:
                ttl = redis.ttl(client_ip)
                detail = {"error": "Too Many Requests", "message": f"Rate limit exceeded. Try again in {ttl} seconds."}
                return JSONResponse(status_code=429, content=detail)

            pipe = redis.pipeline()
            pipe.incr(client_ip)
            pipe.expire(client_ip, TIME_WINDOW)
            pipe.execute()
        finally:
            pass

        response = call_next(request)
        return response
