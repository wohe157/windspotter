from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.security import verify_access_token
from app.repositories.users import get_user_by_id

router = APIRouter(prefix="/users")


@router.get("/{user_id}")
async def get_user_new(
    user_id: str, username: Annotated[str, Depends(verify_access_token)]
):
    user_data = get_user_by_id(user_id)
    print(user_data)
    return {"user_id": user_data.user_id, "email": user_data.email}
