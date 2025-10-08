import datetime as dt
from typing import Annotated, Literal

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from app.core.config import settings

TokenType = Literal["access", "refresh"]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_token(data: dict, token_type: TokenType, expires_delta: dt.timedelta) -> str:
    """Create a new JWT token"""
    payload = data | {
        "exp": dt.datetime.now(dt.timezone.utc) + expires_delta,
        "type": token_type,
    }
    return jwt.encode(
        payload, settings.auth_secret_key, algorithm=settings.auth_jwt_algorithm
    )


def verify_token(token: str, token_type: TokenType) -> dict:
    """Verify and decode a given JWT token"""
    try:
        payload = jwt.decode(
            token, settings.auth_secret_key, algorithms=[settings.auth_jwt_algorithm]
        )
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    if payload.get("type") != token_type:
        raise HTTPException(status_code=401, detail="Invalid token type")
    return payload


def verify_access_token(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    """Verifies the provided access token and return the username of the current user"""
    payload = verify_token(token, "access")
    username = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=401, detail="User does not exist")
    return username
