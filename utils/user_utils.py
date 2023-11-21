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
        user_id = int(dict(request).get('path_params')['user_id'])
        token = token.split(' ')[1]
        payload = jwt_utils.decode_access_token(token)
        if user_id == int(payload['id']):
            return payload
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")    
    except HTTPException as e:
        raise HTTPException(status_code=401, detail=e.detail)
