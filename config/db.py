import os
import sys

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

load_dotenv()

# Set the default values for connecting locally
HOST = os.environ.get("DB_HOSTNAME")
PORT = os.environ.get("DB_PORT")
DBNAME = os.environ.get("DB_NAME")
USERNAME = os.environ.get("DB_USERNAME")
PASSWORD = os.environ.get("DB_PASSWORD")

if "pytest" in sys.modules:
    SQLALCHEMY_DATABASE_URL = "sqlite://"

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

else:
    print("Connecting local server..\n")
    HOST = os.environ["DB_HOSTNAME"]
    PORT = os.environ["DB_PORT"]
    DBNAME = os.environ["DB_NAME"]
    USERNAME = os.environ["DB_USERNAME"]
    PASSWORD = os.environ["DB_PASSWORD"]
    engine = create_engine(f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}/{DBNAME}")

meta = MetaData()

# Test the connection and print the status
try:
    conn = engine.connect()
    print("-------------------------- Database connected ----------------------------")
    print(f"{{ \n\tdb_uri: mysql:{USERNAME}@{HOST}/{DBNAME} \n }}")
    print(
        "\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    )
except Exception as e:
    print(f"Failed to connect to database. Error: {e}")
    raise Exception(f"Failed to connect to database. Error: {e}")

localSession = Session(engine)


def create_local_session() -> Session:
    """Factory function that returns a new session object"""
    engine = create_engine(
        f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base = declarative_base()
