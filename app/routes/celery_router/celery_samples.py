from __future__ import annotations

from fastapi import APIRouter
from fastapi.security import HTTPBearer

from app.celery_tasks.tasks import add
from app.middlewares.request_id_injection import request_id_contextvar

celery_sample_router = APIRouter()
httpBearerScheme = HTTPBearer()


@celery_sample_router.post("/create-task", tags=["Celery-Sample"])
def create_task():
    print("Request ID:", request_id_contextvar.get())
    response = add.delay(10, 20)
    return {"task_id": response.id}
