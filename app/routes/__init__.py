from fastapi import APIRouter

from .home import home_router
from .users import user_router
from. celery_samples import celery_sample

api_router = APIRouter()
api_router.include_router(user_router, prefix="/user")
api_router.include_router(home_router, prefix="/home")
api_router.include_router(celery_sample, prefix="/celery-sample")
__all__ = ["api_router"]
