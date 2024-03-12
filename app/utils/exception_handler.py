import traceback
import asyncio
import random

from fastapi import FastAPI
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from pybreaker import CircuitBreakerError
from dependencies import circuit_breaker
from app.utils.slack_notification_utils import send_slack_message
from app.middlewares.request_id_injection import request_id_contextvar


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder({"message": "Validation error", "detail": exc.errors()[0]["msg"]}),
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"success": False, "message": exc.detail})


async def exception_handler(request: Request, exc: Exception):
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
        content={"success": False, "message": error_message }
    )
