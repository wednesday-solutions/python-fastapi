import json
import os
import sys

from app.config.base import db_settings
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

load_dotenv()

# Set the default values for connecting locally
HOST = db_settings.DB_HOSTNAME
PORT = db_settings.DB_PORT
DBNAME = db_settings.DB_NAME
USERNAME = db_settings.DB_USERNAME
PASSWORD = db_settings.DB_PASSWORD

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
    raise Exception(f"Failed to connect to database. Error: {e}")

localSession = Session(engine)


def create_local_session() -> Session:
    """Factory function that returns a new session object"""
    engine = create_engine(f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base = declarative_base()