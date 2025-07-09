from http.client import HTTPException

from starlette.requests import Request

from app.schemas.auth_schemas import CustomHTTPBearer
from app.schemas.user_roles_schemes import UserRole

oauth2_scheme = CustomHTTPBearer()

def is_admin(request: Request):
    user = request.state.user
    if not user or user['role'] not in (UserRole.admin, UserRole.super_admin):
        raise HTTPException(403, 'You dont have rights')