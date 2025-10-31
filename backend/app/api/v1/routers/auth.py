from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm

from app.core.exceptions import InvalidRefreshTokenException
from app.schemas.auth import AccessToken
from app.schemas.common import Message
from app.services.auth_service import AuthService
from app.services.token_service import TokenService

router = APIRouter(prefix="/auth")


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response
) -> AccessToken:
    """
    Use your email and password to authenticate and issue access and refresh tokens.

    The access token must be set in the Autorization header. When the access token
    expires, a new access token can be requested via `POST /api/v1/auth/refresh` using
    the `refresh_token` cookie.
    """
    access_token, refresh_token = AuthService().login(
        email=form_data.username, password=form_data.password
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
    )
    return AccessToken(access_token=access_token)


@router.post("/refresh")
async def refresh(
    response: Response, refresh_token: Annotated[str | None, Cookie()] = None
) -> AccessToken:
    if not refresh_token:
        raise InvalidRefreshTokenException()
    new_access_token, new_refresh_token = AuthService().refresh(refresh_token)
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
    )
    return AccessToken(access_token=new_access_token)


@router.post("/logout")
async def logout(
    response: Response, refresh_token: Annotated[str | None, Cookie()] = None
) -> Message:
    if refresh_token:
        TokenService().revoke_token(refresh_token)
    response.delete_cookie("refresh_token")
    return Message(message="Logged out")
