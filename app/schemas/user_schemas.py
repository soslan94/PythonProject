from datetime import datetime

from pydantic import BaseModel, validator, EmailStr

from app.schemas.user_roles_schemes import UserRole


class BaseUser(BaseModel):
    email: str #EmailStr
    full_name: str
    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True,
    }
    role: UserRole


class UserCreate(BaseUser):
    password: str

class UserResponse(BaseUser):
    id: int
    created_at: datetime
    role: UserRole


class UserReadById(BaseUser):
    id: id
