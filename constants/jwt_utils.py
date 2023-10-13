from fastapi import HTTPException
import jwt
import datetime
from config.config import get_secret_key

def create_access_token(data: dict):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    return jwt.encode({"exp": expiration, **data}, get_secret_key(), algorithm="HS256")

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, get_secret_key(), algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Signature has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
