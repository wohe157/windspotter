import datetime as dt
from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from pwdlib import PasswordHash

from app.core.config import settings
from app.core.security import create_token, verify_token
from app.models.auth import AccessToken
from app.models.common import Message

# TODO: This is only for testing before setting up an actual db
revoked_refresh_tokens = set()

router = APIRouter(prefix="/auth")
hasher = PasswordHash.recommended()


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response
) -> AccessToken:
    # TODO: add database and hashing
    if form_data.username != "admin" or form_data.password != "secret":
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_token(
        {"sub": form_data.username},
        "access",
        dt.timedelta(minutes=settings.auth_access_token_expire_minutes),
    )
    refresh_token = create_token(
        {"sub": form_data.username},
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
def refresh(response: Response, refresh_token: str = Cookie(None)):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    if refresh_token in revoked_refresh_tokens:
        raise HTTPException(status_code=401, detail="Refresh token reused")

    payload = verify_token(refresh_token, "refresh")
    revoked_refresh_tokens.add(refresh_token)

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
async def logout(response: Response) -> Message:
    response.delete_cookie("refresh_token")
    return Message(message="Logged out")
