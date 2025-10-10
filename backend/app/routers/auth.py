import datetime as dt
from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config import settings
from app.core.security import create_token, verify_password, verify_token
from app.models.auth import AccessToken
from app.models.common import Message
from app.repositories.revoked_refresh_tokens import revoke_token, token_is_revoked
from app.repositories.users import get_user_by_email

router = APIRouter(prefix="/auth")


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response
) -> AccessToken:
    user_data = get_user_by_email(form_data.username)
    if user_data is None or not verify_password(
        form_data.password, user_data.password_hash
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_token(
        {"sub": user_data.user_id},
        "access",
        dt.timedelta(minutes=settings.auth_access_token_expire_minutes),
    )
    refresh_token = create_token(
        {"sub": user_data.user_id},
        "refresh",
        dt.timedelta(days=settings.auth_refresh_token_expire_days),
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
    )
    return AccessToken(access_token=access_token, token_type="bearer")


@router.post("/refresh")
async def refresh(response: Response, refresh_token: str = Cookie(None)):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    if token_is_revoked(refresh_token):
        raise HTTPException(status_code=401, detail="Refresh token reused")

    payload = verify_token(refresh_token, "refresh")
    revoke_token(refresh_token)

    new_access = create_token(
        {"sub": payload["sub"]},
        "access",
        dt.timedelta(minutes=settings.auth_access_token_expire_minutes),
    )
    new_refresh = create_token(
        {"sub": payload["sub"]},
        "refresh",
        dt.timedelta(seconds=settings.auth_refresh_token_expire_days),
    )

    response.set_cookie(
        key="refresh_token",
        value=new_refresh,
        httponly=True,
        secure=True,
        samesite="strict",
    )
    return {"access_token": new_access, "token_type": "bearer"}


@router.post("/logout")
async def logout(response: Response, refresh_token: str = Cookie(None)) -> Message:
    if refresh_token:
        revoke_token(refresh_token)
    response.delete_cookie("refresh_token")
    return Message(message="Logged out")
