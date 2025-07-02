import datetime
import jwt
from asyncpg.pgproto.pgproto import timedelta
from decouple import config
from app.schemas.user_schemas import UserReadById


def create_access_token(user: UserReadById):
    try:
        payload = {"sub": str(user.id), "exp": datetime.datetime.now(datetime.timezone.utc) + timedelta(minutes=120)}

        token = jwt.encode(payload, config('JWT_SECRET'), algorithm="HS256")

        print(f'sgenerennui token - {token}')
        return token
    except Exception as e:
        raise e

