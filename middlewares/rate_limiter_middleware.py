from fastapi import Request, HTTPException
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Callable
from fastapi.responses import JSONResponse

_request_timestamps = defaultdict(list)

MAX_REQUESTS = 10
TIME_WINDOW = 60

async def rate_limit_middleware(request: Request, call_next: Callable):
    global _request_timestamps

    client_ip = request.client.host
    now = datetime.now()

    if client_ip not in _request_timestamps:
        _request_timestamps[client_ip] = []

    # Remove expired timestamps
    _request_timestamps[client_ip] = [
        timestamp for timestamp in _request_timestamps[client_ip]
        if now - timestamp <= timedelta(seconds=TIME_WINDOW)
    ]

    # Check the number of requests
    if len(_request_timestamps[client_ip]) >= MAX_REQUESTS:
        # Provide a more informative HTTP 429 response
        detail = {
            "error": "Too Many Requests",
            "message": f"You have exceeded the maximum number of requests ({MAX_REQUESTS}) in the time window ({TIME_WINDOW}s)."
        }
        return JSONResponse(
            status_code=429,
            content=detail,
        )

    # Log the current request
    _request_timestamps[client_ip].append(now)

    response = await call_next(request)
    return response
