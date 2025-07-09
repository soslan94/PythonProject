from app.schemas.clothes_schemas import ClothesCreate, ClothesResponse
from app.models import clothes
from app.db import database


async def create_clothes(clothes_data: ClothesCreate):
    id_ = await database.execute(clothes.insert().values(**clothes_data.dict()))
    return await database.fetch_one(clothes.select().where(clothes.c.id == id_))