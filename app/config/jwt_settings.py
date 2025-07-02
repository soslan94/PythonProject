import datetime
import jwt
from asyncpg.pgproto.pgproto import timedelta
from app.schemas import UserReadById
from decouple import config

def create_access_token(user: UserReadById):
    try:
        payload = {"sub": user.id, "exp": datetime.datetime.now(datetime.timezone.utc) + timedelta(minutes=120)}
        return jwt.encode(payload, config('JWT_SECRET'), algorithm="HS256")
    except Exception as e:
        raise e