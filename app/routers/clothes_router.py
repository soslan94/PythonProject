from fastapi import APIRouter, HTTPException, Depends

import app.crud.clothes_crud
from app.middleware.jwt_based_auth import oauth2_scheme, is_admin
from app.schemas.clothes_schemas import ClothesCreate, ClothesResponse

clothes_router = APIRouter(prefix="/clothes", tags=["clothes"])

@clothes_router.post('/clothes/',response_model=ClothesResponse,
                     dependencies=[Depends(oauth2_scheme), Depends(is_admin)], status_code=201)
async def create_clothes(clothes_data: ClothesCreate,):
    try:
        return await app.crud.clothes_crud.create_clothes(clothes_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))