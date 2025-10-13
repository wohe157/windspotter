class InvalidOrExpiredTokenError(Exception):
    """Raised when a JWT token is invalid or expired"""


class InvalidCredentialsError(Exception):
    """Raised when email and/or password is incorrect"""
