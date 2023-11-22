import asyncio
import random
from fastapi import FastAPI
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routes.users import user
from fastapi_pagination import add_pagination
from middlewares.rate_limiter_middleware import RateLimitMiddleware
from pybreaker import CircuitBreakerError
from dependencies import circuit_breaker

# Initializing the swagger docs
app = FastAPI(
    title="FastAPI Template",
    description="This is my first API use FastAPI",
    version="0.0.1",
    openapi_tags=[{"name": "FastAPI Template", "description": "API template using FastAPI."}],
)


origins = ["*"]

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RateLimitMiddleware)
app.include_router(user, prefix="/user")


# Default API route
@app.get("/")
async def read_main():
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


@app.get("/{path:path}")
async def catch_all(path: str):
    return JSONResponse(status_code=404, content={"success": False, "message": f"Route not found for path: {path}"})


add_pagination(app)
