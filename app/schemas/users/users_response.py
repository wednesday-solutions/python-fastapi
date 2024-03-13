from pydantic import BaseModel, Field


class UserOutResponse(BaseModel):
    id: int = Field(alias="id")
    name: str
    email: str
    mobile: str

    class Config:
        orm_mode = True
