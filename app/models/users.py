from __future__ import annotations

from sqlalchemy import Column
from sqlalchemy import event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.sql.sqltypes import Integer
from sqlalchemy.sql.sqltypes import String
from werkzeug.security import generate_password_hash

from app.sessions.db import engine

Base = declarative_base()


class User(Base):  # type: ignore
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(String(50), unique=True)
    mobile = Column(String(50), unique=True)
    password = Column(String(200))  # Store the password hash
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)


# Define an event listener to hash the password before inserting a new user
@event.listens_for(User, "before_insert")
def hash_password_before_insert(mapper, connection, target):
    print("IN EVENT LISTENER")
    if target.password:
        target.password = generate_password_hash(target.password, method="pbkdf2")


Base.metadata.create_all(bind=engine)
