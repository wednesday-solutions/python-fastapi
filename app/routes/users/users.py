from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi_pagination import Page
from app.sessions.db import create_local_session
from app.daos.users import (
    create_user as create_user_dao,
    get_user as get_user_dao,
    list_users as list_users_dao,
    login as signin,
)
from app.schemas.users.users_request import CreateUser, Login
from app.schemas.users.users_response import UserOutResponse
from app.utils.user_utils import get_current_user
from typing import Annotated
from fastapi.security import HTTPBearer
from app.middlewares.request_id_injection import request_id_contextvar

user_router = APIRouter()

httpBearerScheme = HTTPBearer()


@user_router.post("/register", tags=["Users"])
def register(payload: CreateUser, db: Session = Depends(create_local_session)):
    print("Request ID:", request_id_contextvar.get())
    response = create_user_dao(data=payload, dbSession=db)
    return response


@user_router.post("/signin", tags=["Users"])
def login(payload: Login, db: Session = Depends(create_local_session)):
    print("Request ID:", request_id_contextvar.get())
    response = signin(data=payload, dbSession=db)
    return response


@user_router.get("/{user_id}", tags=["Users"], dependencies=[Depends(get_current_user)], response_model=UserOutResponse)
def profile(
    token: Annotated[str, Depends(httpBearerScheme)],
    user_id,
    db: Session = Depends(create_local_session),
):
    print("Request ID:", request_id_contextvar.get())
    response = get_user_dao(user_id, dbSession=db)
    return response


@user_router.get("/", tags=["Users"], response_model=Page[UserOutResponse])
def list_users(db: Session = Depends(create_local_session)):
    print("Request ID:", request_id_contextvar.get())
    response = list_users_dao(dbSession=db)
    return response


@user_router.get("/{user_id}/secure-route/", tags=["Users"], dependencies=[Depends(get_current_user)])
def secure_route(token: Annotated[str, Depends(httpBearerScheme)], user_id: int):
    print("Request ID:", request_id_contextvar.get())
    return {"message": "If you see this, you're authenticated"}
