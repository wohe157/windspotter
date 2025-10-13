import datetime as dt
from typing import Literal

from app.core.exceptions import InvalidOrExpiredTokenError
from app.core.security import create_token, decode_token
from app.repositories.revoked_token_repository import RevokedTokenRepository


class TokenService:
    def __init__(self):
        self.revoked_token_repository = RevokedTokenRepository()

    def generate_token(
        self,
        user_id: str,
        token_type: Literal["access", "refresh"],
        expires_delta: dt.timedelta,
    ) -> str:
        """Generate a new token"""
        payload = {
            "sub": user_id,
            "exp": dt.datetime.now(dt.timezone.utc) + expires_delta,
            "type": token_type,
        }
        return create_token(payload)

    def revoke_token(self, token: str) -> None:
        """Revoke a token"""
        self.revoked_token_repository.add_token(token)

    def validate_token(
        self, token: str, token_type: Literal["access", "refresh"]
    ) -> str:
        """Verify that the given token is a valid access or refresh token and return the user ID"""
        if self.revoked_token_repository.is_revoked(token):
            raise InvalidOrExpiredTokenError()

        payload = decode_token(token)
        if payload.get("type") != token_type:
            raise InvalidOrExpiredTokenError()

        user_id = payload.get("sub")
        if user_id is None:
            raise InvalidOrExpiredTokenError()
        return user_id
