from __future__ import annotations

from fastapi import HTTPException
from fastapi import Request
from sqlalchemy.orm import Session

from app.constants import jwt_utils


def response_formatter(message, data=None):
    return {"success": True, "message": message, "data": data}


def check_existing_field(db_session: Session, model, field, value):
    existing = db_session.query(model).filter(getattr(model, field) == value).first()

    if existing:
        return True
    return False


async def get_current_user(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Token not provided")

    try:
        user_id = int(dict(request).get("path_params")["user_id"])  # type: ignore
        token = token.split(" ")[1]
        payload = jwt_utils.decode_access_token(token)
        if user_id == int(payload["id"]):
            return payload
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")
    except HTTPException as e:
        raise HTTPException(status_code=401, detail=e.detail)
