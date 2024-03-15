from __future__ import annotations

import contextvars
import uuid

from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

request_id_contextvar = contextvars.ContextVar("request_id", default=None)  # type: ignore


class RequestIdInjection(BaseHTTPMiddleware):
    def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request_id_contextvar.set(request_id)  # type: ignore
        try:
            return call_next(request)

        except Exception as ex:
            print(ex)
            return JSONResponse(content={"success": False}, status_code=500)

        finally:
            assert request_id_contextvar.get() == request_id
