from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi import Request, HTTPException
from constants import jwt_utils
from fastapi import HTTPException

def responseFormatter(message, data=None):
    return {"success": True, "message": message, "data": data}

def check_existing_field(dbSession: Session, model, field, value):
    existing = dbSession.query(model).filter(getattr(model, field) == value).first()

    if existing:
        return True
    return False

async def get_current_user(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Token not provided")

    try:
        payload = jwt_utils.decode_access_token(token)
        return payload
    except HTTPException:
        raise HTTPException(status_code=401, detail="Invalid Token or Expired")
