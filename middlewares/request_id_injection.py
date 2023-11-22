from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi.responses import JSONResponse
import contextvars
import uuid

request_id_contextvar = contextvars.ContextVar("request_id", default=None)

class RequestIdInjection(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request_id_contextvar.set(request_id)
        try:
            return await call_next(request)

        except Exception as ex:
            print(ex)
            return JSONResponse(content={"success": False}, status_code=500)

        finally:
            assert request_id_contextvar.get() == request_id
