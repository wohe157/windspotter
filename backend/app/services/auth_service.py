import datetime as dt

from app.core.config import settings
from app.core.exceptions import InvalidCredentialsError
from app.core.security import verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.services.token_service import TokenService


class AuthService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.token_service = TokenService()

    def authenticate_user(self, email: str, password: str) -> User | None:
        """Verify the given credentials"""
        user = self.user_repository.get_user_by_email(email)
        if user is None or not verify_password(password, user.password_hash):
            return None
        return user

    def login(self, email: str, password: str) -> tuple[dict, dict]:
        """Authenticate the given credentials and issue an access and a refresh token"""
        user = self.authenticate_user(email, password)
        if not user:
            raise InvalidCredentialsError()
        return self._issue_new_tokens(user.user_id)

    def refresh(self, refresh_token: str) -> tuple[str, str]:
        """Validate the given refresh token and issue new tokens"""
        user_id = self.token_service.validate_token(refresh_token, "refresh")
        self.token_service.revoke_token(refresh_token)
        if user_id is None:
            raise InvalidCredentialsError()
        return self._issue_new_tokens(user_id)

    def _issue_new_tokens(self, user_id: str) -> tuple[str, str]:
        access_token = self.token_service.generate_token(
            user_id,
            "access",
            dt.timedelta(minutes=settings.auth_access_token_expire_minutes),
        )
        refresh_token = self.token_service.generate_token(
            user_id,
            "refresh",
            dt.timedelta(days=settings.auth_refresh_token_expire_days),
        )
        return access_token, refresh_token
