from pydantic import BaseModel


class RevokedToken(BaseModel):
    token: str
