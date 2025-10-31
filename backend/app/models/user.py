from datetime import datetime

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    user_id: str
    name: str | None = None
    email: EmailStr
    password_hash: str
    is_active: bool
    expires_at: datetime | None = None
