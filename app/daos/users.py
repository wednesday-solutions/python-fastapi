from __future__ import annotations

import json

from fastapi import HTTPException
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash

from app.constants import jwt_utils
from app.constants.messages.users import user_messages as messages
from app.exceptions import EmailAlreadyExistException
from app.exceptions import InvalidCredentialsException
from app.exceptions import MobileAlreadyExistException
from app.exceptions import NoUserFoundException
from app.models import User
from app.schemas.users.users_request import CreateUser
from app.schemas.users.users_request import Login
from app.utils.user_utils import check_existing_field
from app.utils.user_utils import response_formatter
from app.wrappers.cache_wrappers import CacheUtils


async def get_user(user_id: int, db_session: Session):
    try:
        if not user_id:
            raise NoUserFoundException(messages["NO_USER_ID_PROVIDED"])

        cache_key = f"user_{user_id}"
        cached_user, _ = await CacheUtils.retrieve_cache(cache_key)
        if cached_user:
            return json.loads(cached_user)
        # Check if the user already exists in the database
        user = (
            db_session.query(User)
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
        if not user:
            raise NoUserFoundException(messages["NO_USER_FOUND_FOR_ID"])

        await CacheUtils.create_cache(json.dumps(user._asdict(), default=str), cache_key, 60)
        return user._asdict()
    except Exception as e:
        # Return a user-friendly error message to the client
        raise HTTPException(status_code=400, detail=f"{str(e)}")


def list_users(db_session: Session):
    try:
        query = select(User.id, User.name, User.email, User.mobile).order_by(User.created_at)

        # Pass the Select object to the paginate function
        users = paginate(db_session, query=query)

        return users

    except Exception as e:
        print(e)
        # Return a user-friendly error message to the client
        raise HTTPException(status_code=400, detail=f"{str(e)}")


def create_user(data: CreateUser, db_session: Session):
    try:
        user_data = data.dict()
        # Check if the email already exists in the db
        email_exists = check_existing_field(
            db_session=db_session,
            model=User,
            field="email",
            value=user_data["email"],
        )
        if email_exists:
            print("Email already exists", email_exists)
            raise EmailAlreadyExistException(messages["EMAIL_ALREADY_EXIST"])

        # Check if the mobile already exists in the db
        mobile_exists = check_existing_field(
            db_session=db_session,
            model=User,
            field="mobile",
            value=user_data["mobile"],
        )
        if mobile_exists:
            raise MobileAlreadyExistException(messages["MOBILE_ALREADY_EXIST"])

        user = User(**user_data)

        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        return response_formatter(messages["CREATED_SUCCESSFULLY"])

    except Exception as e:
        # Return a user-friendly error message to the client
        raise HTTPException(status_code=400, detail=f"{str(e)}")


def login(data: Login, db_session: Session):
    try:
        user_data = data.dict()

        # Check if the course already exists in the db
        user_details = (
            db_session.query(User)
            .where(
                User.email == user_data["email"],
            )
            .first()
        )

        if not user_details:
            raise InvalidCredentialsException(messages["NO_USERS_FOUND_IN_DB"])

        if not check_password_hash(user_details.password, user_data["password"]):
            raise InvalidCredentialsException(messages["INVALID_CREDENTIALS"])

        token = jwt_utils.create_access_token({"sub": user_details.email, "id": user_details.id})
        return response_formatter(messages["LOGIN_SUCCESSFULLY"], {"token": token})

    except Exception as e:
        print(e)
        # Return a user-friendly error message to the client
        raise HTTPException(status_code=400, detail=f"{str(e)}")
