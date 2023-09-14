from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from config.db import create_local_session
from daos.users import create_user as create_user_dao
from daos.users import get_user as get_user_dao
from daos.users import login as signin
from schemas.users import CreateUser
from schemas.users import Login

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
