from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    name: str | None = None


class User(UserBase):
    user_id: str
    password_hash: str


class UserCreate(UserBase):
    password: str
