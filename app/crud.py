from .db import database
from .models import users
from .schemas import UserCreate

async def create_user(user: UserCreate) -> int:
    query = users.insert().values(**user.dict())
    return await database.execute(query)

async def get_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)