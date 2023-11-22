from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi_pagination import Page
from config.db import create_local_session
from daos.users import create_user as create_user_dao
from daos.users import get_user as get_user_dao
from daos.users import list_users as list_users_dao
from daos.users import login as signin
from models.users import User
from schemas.users import CreateUser
from schemas.users import UserOutResponse
from schemas.users import Login
from utils.redis_utils import get_redis
from utils.user_utils import get_current_user
from typing import Annotated
from fastapi.security import HTTPBearer
from middlewares.request_id_injection import request_id_contextvar

user = APIRouter()

httpBearerScheme = HTTPBearer()


@user.post("/register", tags=["Users"])
def register(payload: CreateUser, db: Session = Depends(create_local_session)):
    print('Request ID:', request_id_contextvar.get())
    response = create_user_dao(data=payload, dbSession=db)
    return response


@user.post("/signin", tags=["Users"])
def login(payload: Login, db: Session = Depends(create_local_session)):
    print('Request ID:', request_id_contextvar.get())
    response = signin(data=payload, dbSession=db)
    return response


@user.get("/{user_id}", tags=["Users"], dependencies=[Depends(get_current_user)])
def profile(
    token: Annotated[str, Depends(httpBearerScheme)],
    user_id,
    db: Session = Depends(create_local_session),
    redis_instance=Depends(get_redis),
):
    print('Request ID:', request_id_contextvar.get())
    # Here, you can use 'redis' to fetch or store data in Redis cache
    response = get_user_dao(user_id, dbSession=db)
    return response


@user.get("/", tags=["Users"], response_model=Page[UserOutResponse])
def list_users(db: Session = Depends(create_local_session)):
    print('Request ID:', request_id_contextvar.get())
    response = list_users_dao(dbSession=db)
    return response


@user.get("/{user_id}/secure-route/", tags=["Users"], dependencies=[Depends(get_current_user)])
def secure_route(token: Annotated[str, Depends(httpBearerScheme)], user_id: int):
    print('Request ID:', request_id_contextvar.get())
    return {"message": "If you see this, you're authenticated"}
