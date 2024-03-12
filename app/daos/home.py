import asyncio
import random

from fastapi.exceptions import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.middlewares.rate_limiter_middleware import RateLimitMiddleware
from app.middlewares.request_id_injection import (
    RequestIdInjection,
    request_id_contextvar
)
from pybreaker import CircuitBreakerError
from dependencies import circuit_breaker
from app.utils.slack_notification_utils import send_slack_message


async def external_service_call():
    # Simulate network delay
    delay = random.uniform(0.1, 1.0)  # Random delay between 0.1 to 1.0 seconds
    await asyncio.sleep(delay)

    # Simulate occasional failures
    if random.random() < 0.2:  # 20% chance of failure
        raise Exception("External service failed")

    return "Success from external service"

