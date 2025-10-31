from typing import Annotated

from app.api.v1.dependencies import CurrentUser
from app.schemas.common import Message
from app.schemas.user import UserData, UserNew, UserUpdates
from app.services.user_service import UserService
from fastapi import APIRouter, Form

router = APIRouter(prefix="/users")


@router.post("/register")
async def register(credentials: Annotated[UserNew, Form()]) -> Message:
    UserService().register(email=credentials.email, password=credentials.password)
    return Message(message="Registered succesfully.")


@router.get("/me")
async def get_user(user: CurrentUser) -> UserData:
    return UserData(user_id=user.user_id, name=user.name, email=user.email)


@router.patch("/me")
async def update_user(
    user: CurrentUser, updates: Annotated[UserUpdates, Form()]
) -> Message:
    UserService().update_user_data(
        user_id=user.user_id,
        name=updates.name,
        email=updates.email,
        password=updates.password,
    )
    return Message(message="User has been updated.")


@router.delete("/me")
async def delete_user(user: CurrentUser) -> Message:
    UserService().delete_user(user.user_id)
    return Message(message="User has been marked for deletion.")
