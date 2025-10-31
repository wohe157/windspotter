class InvalidAccessTokenException(Exception):
    pass


class InvalidRefreshTokenException(Exception):
    pass


class InvalidCredentialsException(Exception):
    pass


class ItemNotFoundException(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)
        self.msg = msg


class ItemAlreadyExistsException(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)
        self.msg = msg
