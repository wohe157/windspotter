import jwt
from pwdlib import PasswordHash

from app.core.config import settings
from app.core.exceptions import InvalidOrExpiredTokenError

_password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return _password_hasher.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return _password_hasher.verify(plain, hashed)


def create_token(payload: dict) -> str:
    return jwt.encode(
        payload, settings.auth_secret_key, algorithm=settings.auth_jwt_algorithm
    )


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(
            token, settings.auth_secret_key, algorithms=[settings.auth_jwt_algorithm]
        )
    except jwt.exceptions.PyJWTError as e:
        raise InvalidOrExpiredTokenError() from e
