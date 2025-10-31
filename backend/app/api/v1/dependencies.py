from typing import Annotated

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.services.token_service import TokenService
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    user_id = TokenService().validate_token(token, "access")
    user = UserRepository().get_user_by_id(user_id)
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
