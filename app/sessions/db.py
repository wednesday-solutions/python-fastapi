from __future__ import annotations

import json
import os
import sys
from collections.abc import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.config.base import settings
from app.exceptions import DatabaseConnectionException

load_dotenv()

# Set the default values for connecting locally
HOST = settings.DB_HOSTNAME
PORT = settings.DB_PORT
DBNAME = settings.DB_NAME
USERNAME = settings.DB_USERNAME
PASSWORD = settings.DB_PASSWORD

if "pytest" in sys.modules:
    SQLALCHEMY_DATABASE_URL = "sqlite://"

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

elif "PYTHON_FASTAPI_TEMPLATE_CLUSTER_SECRET" in os.environ:
    print("Connecting to database on RDS..\n")
    dbSecretJSON = os.environ["PYTHON_FASTAPI_TEMPLATE_CLUSTER_SECRET"]
    dbSecretParsed = json.loads(dbSecretJSON)

    HOST = dbSecretParsed["host"]
    PORT = dbSecretParsed["port"]
    DBNAME = dbSecretParsed["dbname"]
    USERNAME = dbSecretParsed["username"]
    PASSWORD = dbSecretParsed["password"]

    engine = create_engine(f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}/{DBNAME}")

else:
    print("Connecting local database..\n")
    engine = create_engine(f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}/{DBNAME}")

meta = MetaData()

# Test the connection and print the status


try:
    conn = engine.connect()
    print("-------------------------- Database connected ----------------------------")
    print(f"{{ \n\tdb_uri: mysql:{USERNAME}@{HOST}/{DBNAME} \n }}")
    print("\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
except Exception as e:
    print(f"Failed to connect to database. Error: {e}")
    raise DatabaseConnectionException("Failed to connect to database")

localSession = Session(engine)


def create_local_session() -> Generator[Session, None, None]:
    """Factory function that returns a new session object"""
    engine = create_engine(f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}")
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = session_local()
    try:
        yield db
    finally:
        db.close()


Base = declarative_base()
