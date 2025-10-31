from fastapi import FastAPI

from app.api.v1.routers import auth, users
from app.core.config import settings
from app.handlers.exception_handlers import register_exception_handlers

API_V1_PREFIX = "/api/v1"

app = FastAPI(title=settings.app_name)
app.include_router(auth.router, prefix=API_V1_PREFIX)
app.include_router(users.router, prefix=API_V1_PREFIX)

register_exception_handlers(app)
