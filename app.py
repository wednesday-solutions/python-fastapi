from fastapi import FastAPI
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routes.users import user
import config.db

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

app.include_router(user, prefix='/user')

# Default API route
@app.get("/")
async def read_main():
    return {"response": "service up and running..!"}


# pylint: disable=unused-argument
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder(
            {"message": "Validation error", "detail": exc.errors()[0]["msg"]}
        ),
    )


# pylint: disable=unused-argument
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code, content={"success": False, "message": exc.detail }
    )

@app.get("/{path:path}")
async def catch_all(path: str):
    return JSONResponse(
        status_code=404, content={"success": False, "message": f"Route not found for path: {path}"}
    )
