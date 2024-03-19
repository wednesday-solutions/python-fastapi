from __future__ import annotations

import random

from fastapi import APIRouter
from fastapi.security import HTTPBearer

from app.middlewares.request_id_injection import request_id_contextvar

cache_sample_router = APIRouter()
httpBearerScheme = HTTPBearer()


@cache_sample_router.get("/get-cache", tags=["Cache-Sample"])
def get_cache():
    print("Request ID:", request_id_contextvar.get())
    response = random.randint(100, 1000)  # NOSONAR
    return {"random value is": response}
