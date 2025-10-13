from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.exceptions import InvalidCredentialsError
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
    try:
        access_token, refresh_token = AuthService().login(
            email=form_data.username, password=form_data.password
        )
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email and/or password",
            headers={"WWW-Authenticate": "Bearer"},
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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Missing refresh token"
        )
    try:
        new_access_token, new_refresh_token = AuthService().refresh(refresh_token)
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid refresh token"
        )

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
