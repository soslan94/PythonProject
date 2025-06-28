from datetime import datetime

from pydantic import BaseModel, validator, EmailStr
#from email_validator import validate_email, EmailNotValidError

# class EmailField(str):
#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate
#
#     @classmethod
#     def validate(cls, v) -> str:
#         try:
#             validate_email(v)
#             return v
#         except EmailNotValidError:
#             raise ValueError('Invalid email')

class BaseUser(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(BaseUser):
    password: str

class UserRead(BaseUser):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True