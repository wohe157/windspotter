from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    InvalidAccessTokenException,
    InvalidCredentialsException,
    InvalidRefreshTokenException,
    ItemAlreadyExistsException,
    ItemNotFoundException,
)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(InvalidCredentialsException)
    async def _(request: Request, exc: InvalidCredentialsException) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={"detail": "Invalid credentials"},
            headers={"WWW-Authenticate": "Bearer"},
        )

    @app.exception_handler(InvalidAccessTokenException)
    async def _(request: Request, exc: InvalidAccessTokenException) -> JSONResponse:
        return JSONResponse(
            status_code=401,
            content={"detail": "Invalid authentication credentials"},
            headers={"WWW-Authenticate": "Bearer"},
        )

    @app.exception_handler(InvalidRefreshTokenException)
    async def _(request: Request, exc: InvalidRefreshTokenException) -> JSONResponse:
        return JSONResponse(
            status_code=401, content={"detail": "Invalid refresh token"}
        )

    @app.exception_handler(ItemNotFoundException)
    async def _(request: Request, exc: ItemNotFoundException) -> JSONResponse:
        return JSONResponse(status_code=404, content={"detail": exc.msg})

    @app.exception_handler(ItemAlreadyExistsException)
    async def _(request: Request, exc: ItemAlreadyExistsException) -> JSONResponse:
        return JSONResponse(status_code=409, content={"detail": exc.msg})
