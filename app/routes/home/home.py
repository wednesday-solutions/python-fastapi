from __future__ import annotations

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from pybreaker import CircuitBreakerError

from app.config.base import settings
from app.daos.home import external_service_call
from app.exceptions import CentryTestException
from app.middlewares.request_id_injection import request_id_contextvar
from dependencies import circuit_breaker

home_router = APIRouter()


@home_router.get("/", tags=["Home"])
async def read_main():
    print("Request ID:", request_id_contextvar.get())
    return {"response": "service up and running..!"}


@home_router.get("/external-service", tags=["Home"])
async def external_service_endpoint():
    try:
        with circuit_breaker.calling():
            result = await external_service_call()
            return {"message": result}
    except CircuitBreakerError:
        raise HTTPException(status_code=503, detail="Service temporarily unavailable")
    except Exception as e:
        # Handle other exceptions from the external service call
        raise HTTPException(status_code=500, detail=str(e))


@home_router.get("/sentry-test", tags=["Home"])
def sentry_endpoint():
    if not settings.SENTRY_DSN:
        raise HTTPException(status_code=503, detail="Sentry is not enabled")
    raise CentryTestException("Sentry Test")


@home_router.get("/{path:path}", include_in_schema=False)
async def catch_all(path: str):
    return JSONResponse(status_code=404, content={"success": False, "message": f"Route not found for path: {path}"})
