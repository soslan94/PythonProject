from fastapi import APIRouter, HTTPException
from . import crud, schemas

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register/", response_model=schemas.UserRead)
async def register(user: schemas.UserCreate):
    try:
        user_id = await crud.create_user(user)
        record = await crud.get_user(user_id)
        if not record:
            raise HTTPException(status_code=404, detail="User not found")
        return record
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))