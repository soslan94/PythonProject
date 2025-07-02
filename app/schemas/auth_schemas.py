from fastapi import HTTPException
from decouple import config
import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.requests import Request


from app.db import database
from app.models import users


class CustomHTTPBearer(HTTPBearer):

    async def __call__(
        self, request: Request
    ) -> HTTPAuthorizationCredentials:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        token = credentials.credentials
        try:
            payload = jwt.decode(
                token,
                config("JWT_SECRET"),
                algorithms=["HS256"],
                options={"require_sub": True, "require_exp": True},
            )
            user_id = int(payload["sub"])

            query = users.select().where(users.c.id == user_id)
            user = await database.fetch_one(query)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            request.state.user = user

            return credentials

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except (jwt.InvalidTokenError, KeyError, ValueError):
            raise HTTPException(status_code=401, detail="Invalid token")