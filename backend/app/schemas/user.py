from pydantic import BaseModel, EmailStr


class UserData(BaseModel):
    user_id: str
    name: str | None
    email: EmailStr


class UserNew(BaseModel):
    model_config = {"extra": "forbid"}

    email: EmailStr
    password: str


class UserUpdates(BaseModel):
    model_config = {"extra": "forbid"}

    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
