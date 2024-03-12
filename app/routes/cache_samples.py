import random
from fastapi import APIRouter
from app.celery_tasks.tasks import add
from fastapi.security import HTTPBearer
from app.middlewares.request_id_injection import request_id_contextvar

cache_sample = APIRouter()
httpBearerScheme = HTTPBearer()

@cache_sample.get("/get-cache", tags=["Cache-Sample"])
def get_cache():
    print('Request ID:', request_id_contextvar.get())
    response = random.randint(100,1000)
    return {"random value is": response}
