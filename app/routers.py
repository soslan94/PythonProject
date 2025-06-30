from typing import List

from fastapi import APIRouter, HTTPException
from . import crud
from .schemas import UserResponse, UserCreate

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register/", response_model=UserResponse)
async def register(user: UserCreate):
    try:
        return await crud.create_user(user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/users/", response_model=List[UserResponse])
async def users_get():
    try:
        return await crud.get_users()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Could not fetch users")

@router.get("/users/{id}/", response_model=UserResponse)
async def user_get(id: int):
    try:
        return await crud.get_user(id)
    except Exception as e:
        raise HTTPException(status_code=404, detail='user does not exist')