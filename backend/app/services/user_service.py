from app.core.security import hash_password
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    # TODO: add email verification
    def register(self, email: str, password: str) -> None:
        self.user_repository.create_user(
            email=email, password_hash=hash_password(password)
        )

    # TODO: send email for confirmation
    def delete_user(self, user_id: str) -> None:
        self.user_repository.delete_user(user_id)

    def update_user_data(
        self,
        user_id: str,
        name: str | None = None,
        email: str | None = None,
        password: str | None = None,
    ) -> None:
        self.user_repository.update_user_data(
            user_id=user_id,
            name=name,
            email=email,
            password_hash=hash_password(password) if password is not None else None,
        )
