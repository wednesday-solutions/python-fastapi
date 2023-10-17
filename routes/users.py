from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from config.db import create_local_session
from daos.users import create_user as create_user_dao
from daos.users import get_user as get_user_dao
from daos.users import login as signin
from schemas.users import CreateUser
from schemas.users import Login
from utils.user_utils import get_current_user

user = APIRouter()

@user.post("/register", tags=["Users"])
def register(payload: CreateUser, db: Session = Depends(create_local_session)):
    response = create_user_dao(data=payload, dbSession=db)
    return response

@user.post("/signin", tags=["Users"])
def login(payload: Login, db: Session = Depends(create_local_session)):
    response = signin(data=payload, dbSession=db)
    return response

@user.get("/{user_id}", tags=["Users"])
def profile(user_id, db: Session = Depends(create_local_session)):
    response = get_user_dao(user_id, dbSession=db)
    return response


@user.get("/secure-route/", tags=["Users"], dependencies=[Depends(get_current_user)])
def secure_route():
    return {"message": "If you see this, you're authenticated"}
