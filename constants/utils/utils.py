from fastapi import HTTPException
from sqlalchemy.orm import Session

def responseFormatter(message, data=None):
    return {"success": True, "message": message, "data": data}

def check_existing_field(dbSession: Session, model, field, value):
    existing = dbSession.query(model).filter(getattr(model, field) == value).first()

    if existing:
        return True
    return False