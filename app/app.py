import asyncio
import random
from fastapi import FastAPI
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.celery_tasks.tasks import add
from app.routes.users import user
from app.routes.celery_samples import celery_sample
from app.config.base import settings
from app.config.celery_utils import create_celery
from fastapi_pagination import add_pagination
from app.middlewares.rate_limiter_middleware import RateLimitMiddleware
from app.middlewares.request_id_injection import RequestIdInjection
from pybreaker import CircuitBreakerError
from dependencies import circuit_breaker
from app.utils.slack_notification_utils import send_slack_message
import traceback
from app.middlewares.request_id_injection import request_id_contextvar


app = FastAPI(
    title="FastAPI Template",
    description="This is my first API use FastAPI",
    version="0.0.1",
    openapi_tags=[{"name": "FastAPI Template", "description": "API template using FastAPI."}],
)
celery = create_celery()
origins = settings.ALLOWED_HOSTS

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(RequestIdInjection)
app.include_router(user, prefix="/user")
app.include_router(celery_sample,prefix='/celery-samples')
# Default API route
@app.get("/")
async def read_main():
    print('Request ID:', request_id_contextvar.get())
    return {"response": "service up and running..!"}


async def external_service_call():
    # Simulate network delay
    delay = random.uniform(0.1, 1.0)  # Random delay between 0.1 to 1.0 seconds
    await asyncio.sleep(delay)

    # Simulate occasional failures
    if random.random() < 0.2:  # 20% chance of failure
        raise Exception("External service failed")

    return "Success from external service"


@app.get("/external-service")
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


# pylint: disable=unused-argument
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder({"message": "Validation error", "detail": exc.errors()[0]["msg"]}),
    )


# pylint: disable=unused-argument
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"success": False, "message": exc.detail})


@app.exception_handler(Exception)
async def http_exception_handler(request: Request, exc: Exception):
    error_message = f'Error: {str(exc)}'
    # Include the traceback in the response for debugging purposes
    traceback_str = traceback.format_exc(chain=False)
    send_slack_message(
        {
            "text": f'```\nRequestID: {request_id_contextvar.get()}\nRequest URL: {str(request.url)} \nRequest_method: {str(request.method)} \nTraceback: {traceback_str}```'
        }
    )

    return JSONResponse(
        status_code=500,
        content={"success": False, "message": error_message}
    )


@app.get("/{path:path}")
async def catch_all(path: str):
    return JSONResponse(status_code=404, content={"success": False, "message": f"Route not found for path: {path}"})


add_pagination(app)
