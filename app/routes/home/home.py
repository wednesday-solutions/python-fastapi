from fastapi import APIRouter
from fastapi import Depends
from app.models import User
from app.schemas.users.users_request import CreateUser, Login
from app.schemas.users.users_response import UserOutResponse
from app.utils.redis_utils import get_redis
from app.utils.user_utils import get_current_user
from typing import Annotated
from fastapi.security import HTTPBearer
from app.middlewares.request_id_injection import request_id_contextvar
from app.daos.home import external_service_call

home_router = APIRouter()

@home_router.get("/", tags=["Home"])
async def read_main():
    print('Request ID:', request_id_contextvar.get())
    return {"response": "service up and running..!"}



@home_router.get("/external-service", tags=["Home"])
async def external_service_endpoint():
    try:
        with circuit_breaker:
            result = await external_service_call()
            return {"message": result}
    except CircuitBreakerError:
        raise HTTPException(status_code=503, detail="Service temporarily unavailable")
    except Exception as e:
        # Handle other exceptions from the external service call
        raise HTTPException(status_code=500, detail=str(e))



@home_router.get("/{path:path}", include_in_schema=False)
async def catch_all(path: str):
    return JSONResponse(status_code=404, content={"success": False, "message": f"Route not found for path: {path}"})
