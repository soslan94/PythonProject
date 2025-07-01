from typing import List

from app.db import database
from app.security import pwd_context
from app.models import users
from app.schemas import UserCreate, UserResponse


async def create_user(user: UserCreate) -> UserResponse:
    user.password = pwd_context.hash(user.password)
    q = users.insert().values(**user.dict())
    new_id = await database.execute(q)
    row = await database.fetch_one(users.select().where(users.c.id == new_id))
    if not row:
        raise RuntimeError('User creation failed')
    return UserResponse(**row)


async def get_users() -> List[UserResponse]:
    rows = await database.fetch_all(users.select())
    return [UserResponse(**row) for row in rows]


async def get_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)