from __future__ import annotations

import asyncio
import random

from app.exceptions import ExternalServiceException


async def external_service_call():
    # Simulate network delay
    delay = random.uniform(0.1, 1.0)  # Random delay between 0.1 to 1.0 seconds  #NOSONAR
    await asyncio.sleep(delay)

    # Simulate occasional failures
    if random.random() < 0.2:  # 20% chance of failure #NOSONAR
        raise ExternalServiceException("External Service Failed")

    return "Success from external service"
