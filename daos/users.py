import json
from fastapi import HTTPException
from sqlalchemy.orm import Session
from constants import jwt_utils
from constants.messages.users import user_messages as messages
from models.users import User
from schemas.users import CreateUser
from schemas.users import Login
from schemas.users import UserOutResponse
from werkzeug.security import check_password_hash
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from utils import redis_utils
from utils.user_utils import check_existing_field, responseFormatter
from datetime import datetime


class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)

def get_user(user_id: int, dbSession: Session):
    try:
        cache_key = f"user:{user_id}"
        cached_user = redis_utils.get_redis().get(cache_key)

        if cached_user:
            return json.loads(cached_user)
        # Check if the subject already exists in the database
        user = (
            dbSession.query(User)
            .filter(User.id == user_id)
            .first()
        )
        if user:
            # Convert the User object to a dictionary with ISO-formatted dates
            user_dict = {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "mobile": user.mobile,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "updated_at": user.updated_at.isoformat() if user.updated_at else None,
                "deleted_at": user.deleted_at.isoformat() if user.deleted_at else None,
            }

            redis_utils.get_redis().set(cache_key, json.dumps(user_dict, cls=CustomEncoder))

            return responseFormatter(messages["USER_DETAILS"], user_dict)

        if not user:
            raise Exception(messages["NO_USER_FOUND_FOR_ID"])

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
