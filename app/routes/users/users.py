from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Path
from fastapi.security import HTTPBearer
from fastapi_pagination import Page
from sqlalchemy.orm import Session

from app.daos.users import create_user as create_user_dao
from app.daos.users import get_user as get_user_dao
from app.daos.users import list_users as list_users_dao
from app.daos.users import login as signin
from app.schemas.users.users_request import CreateUser
from app.schemas.users.users_request import Login
from app.schemas.users.users_response import UserOutResponse
from app.sessions.db import create_local_session
from app.utils.user_utils import get_current_user

user_router = APIRouter()

httpBearerScheme = HTTPBearer()


@user_router.post("/register", tags=["Users"])
def register(payload: CreateUser, db: Session = Depends(create_local_session)):
    response = create_user_dao(data=payload, db_session=db)
    return response


@user_router.post("/signin", tags=["Users"])
def login(payload: Login, db: Session = Depends(create_local_session)):
    response = signin(data=payload, db_session=db)
    return response


@user_router.get("/{user_id}", tags=["Users"], dependencies=[Depends(get_current_user)], response_model=UserOutResponse)
async def profile(
    token: Annotated[str, Depends(httpBearerScheme)],
    user_id: int = Path(..., title="ID of the user"),
    db: Session = Depends(create_local_session),
):
    response = await get_user_dao(user_id, db_session=db)
    return response


@user_router.get("/", tags=["Users"], response_model=Page[UserOutResponse])
def list_users(db: Session = Depends(create_local_session)):
    response = list_users_dao(db_session=db)
    return response


@user_router.get("/{user_id}/secure-route/", tags=["Users"], dependencies=[Depends(get_current_user)])
def secure_route(token: Annotated[str, Depends(httpBearerScheme)], user_id: int):
    return {"message": "If you see this, you're authenticated"}
