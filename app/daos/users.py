import json
import pickle

from redis import Redis
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.constants import jwt_utils
from app.constants.messages.users import user_messages as messages
from app.models import User
from app.schemas.users.users_request import CreateUser, Login
from app.schemas.users.users_response import UserOutResponse
from werkzeug.security import check_password_hash
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from app.utils.user_utils import check_existing_field, responseFormatter

def get_user(user_id: int, dbSession: Session):
    try:
        cache_key = f"user:{user_id}"

        cached_user = Redis().get(cache_key)
        if cached_user:
            return pickle.loads(cached_user)
        # Check if the subject already exists in the database
        user = (
            dbSession.query(User)
            .where(User.id == user_id)
            .with_entities(
                User.id,
                User.name,
                User.email,
                User.mobile,
                User.created_at,
                User.updated_at,
                User.deleted_at,
            )
            .first()
        )
        if user:
            Redis().set(cache_key, pickle.dumps(user))
        if not user:
            raise Exception(messages["NO_USER_FOUND_FOR_ID"])

        return user

    except Exception as e:
        # Return a user-friendly error message to the client
        raise HTTPException(status_code=400, detail=f"{str(e)}")


def list_users(dbSession: Session):
    try:
        query = select(User.id, User.name, User.email, User.mobile).order_by(User.created_at)

        # Pass the Select object to the paginate function
        users = paginate(dbSession, query=query)

        return users

    except Exception as e:
        print(e)
        # Return a user-friendly error message to the client
        raise HTTPException(status_code=400, detail=f"{str(e)}")


def create_user(data: CreateUser, dbSession: Session):
    try:
        user_data = data.dict()
        # Check if the email already exists in the db
        email_exists = check_existing_field(dbSession=dbSession, model=User, field="email", value=user_data["email"])
        if email_exists:
            raise Exception(messages["EMAIL_ALREADY_EXIST"])

        # Check if the mobile already exists in the db
        mobile_exists = check_existing_field(dbSession=dbSession, model=User, field="mobile", value=user_data["mobile"])
        if mobile_exists:
            raise Exception(messages["MOBILE_ALREADY_EXIST"])

        user = User(**user_data)

        dbSession.add(user)
        dbSession.commit()
        dbSession.refresh(user)

        return responseFormatter(messages["CREATED_SUCCESSFULLY"])

    except Exception as e:
        # Return a user-friendly error message to the client
        raise HTTPException(status_code=400, detail=f"{str(e)}")


def login(data: Login, dbSession: Session):
    try:
        user_data = data.dict()

        # Check if the course already exists in the db
        user_details = (
            dbSession.query(User)
            .where(
                User.email == user_data["email"],
            )
            .first()
        )

        if not user_details:
            raise Exception(messages["INVALID_CREDENTIALS"])

        if not check_password_hash(user_details.password, user_data["password"]):
            raise Exception(messages["INVALID_CREDENTIALS"])

        del user_details.password
        token = jwt_utils.create_access_token({"sub": user_details.email, "id": user_details.id})
        return responseFormatter(messages["LOGIN_SUCCESSFULLY"], {"token": token})

    except Exception as e:
        print(e)
        # Return a user-friendly error message to the client
        raise HTTPException(status_code=400, detail=f"{str(e)}")
