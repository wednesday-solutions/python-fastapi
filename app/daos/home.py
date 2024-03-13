import asyncio
import random


async def external_service_call():
    # Simulate network delay
    delay = random.uniform(0.1, 1.0)  # Random delay between 0.1 to 1.0 seconds
    await asyncio.sleep(delay)

    # Simulate occasional failures
    if random.random() < 0.2:  # 20% chance of failure
        raise Exception("External service failed")

    return "Success from external service"
