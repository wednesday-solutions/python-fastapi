import re

from constants.messages.users import user_messages as messages
from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import validator
from email_validator import validate_email
from pydantic import Field


class CreateUser(BaseModel):
    name: str
    email: str
    mobile: str
    password: str

    @validator("name")
    def validate_name(cls, name):
        if len(name) < 3:
            raise ValueError("Name must be at least 3 characters long")
        return name

    @validator("mobile")
    def validate_mobile(cls, mobile):
        if not mobile.isdigit() or len(mobile) != 10:
            raise ValueError("Mobile number must be 10 digits long")
        return mobile

    @validator("email")
    def validate_email(cls, email):
        if not validate_email(email):
            raise ValueError("Invalid email address format")
        return email

    @validator("password")
    def validate_password_strength(cls, password):
        if (
            len(password) < 8
            or not any(char.isupper() for char in password)
            or not any(char.islower() for char in password)
            or not any(char.isdigit() for char in password)
            or not re.search(
                r'[!@#$%^&*(),.?":{}|<>]', password
            )  # The regular expression [!@#$%^&*(),.?":{}|<>] matches any of these special characters.
        ):
            raise ValueError(
                "Password must be strong: at least 8 characters, containing at least one uppercase letter, one lowercase letter, one digit, and one special character."
            )
        return password


class Login(BaseModel):
    email: str
    password: str

    @validator("email")
    def validate_email(cls, email):
        if not validate_email(email):
            raise ValueError("Invalid email address format")
        return email

    @validator("password")
    def validate_password_strength(cls, password):
        if (
            len(password) < 8
            or not any(char.isupper() for char in password)
            or not any(char.islower() for char in password)
            or not any(char.isdigit() for char in password)
            or not re.search(
                r'[!@#$%^&*(),.?":{}|<>]', password
            )  # The regular expression [!@#$%^&*(),.?":{}|<>] matches any of these special characters.
        ):
            raise HTTPException(status_code=400, detail=f"{str(messages['INVALID_CREDENTIALS'])}")
        return password

class UserOutResponse(BaseModel):
    id: int = Field(alias='id')
    name: str
    email: str
    mobile: str
    class Config:
        orm_mode = True
