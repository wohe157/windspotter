from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.exceptions import InvalidOrExpiredTokenError
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.services.token_service import TokenService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    try:
        user_id = TokenService().validate_token(token, "access")
    except InvalidOrExpiredTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = UserRepository().get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not found"
        )
    return user


GetCurrentUserDependency = Annotated[User, Depends(get_current_user)]
