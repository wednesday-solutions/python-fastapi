import re

from pydantic import BaseModel
from pydantic import Field


class UserOutResponse(BaseModel):
    id: int = Field(alias="id")
    name: str
    email: str
    mobile: str

    class Config:
        orm_mode = True
