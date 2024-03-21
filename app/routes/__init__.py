from __future__ import annotations

from fastapi import APIRouter

from .cache_router import cache_sample_router
from .celery_router import celery_sample_router
from .home import home_router
from .users import user_router

api_router = APIRouter()
api_router.include_router(user_router, prefix="/users")
api_router.include_router(home_router, prefix="/home")
api_router.include_router(celery_sample_router, prefix="/celery-sample")
api_router.include_router(cache_sample_router, prefix="/cache-sample")
__all__ = ["api_router"]
