from fastapi import APIRouter

from .home import home_router
from .users import user_router


api_router = APIRouter()
api_router.include_router(user_router, prefix="/user")
api_router.include_router(home_router, prefix="/home")

__all__ = ["api_router"]
