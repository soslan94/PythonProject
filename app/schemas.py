from datetime import datetime

from pydantic import BaseModel, validator, EmailStr

class BaseUser(BaseModel):
    email: str #EmailStr
    full_name: str
    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True,
    }


class UserCreate(BaseUser):
    password: str

class UserResponse(BaseUser):
    id: int
    created_at: datetime


class UserReadById(BaseUser):
    id: id
