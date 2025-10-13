from app.core.config import settings
from app.db.database import get_dynamodb_table
from app.models.revoked_token import RevokedToken


class RevokedTokenRepository:
    def __init__(self):
        self.table = get_dynamodb_table(settings.dynamodb_revoked_refresh_tokens)

    def add_token(self, token: str) -> None:
        item = RevokedToken(token=token)
        self.table.put_item(Item=item.dict())

    def is_revoked(self, token: str) -> bool:
        response = self.table.get_item(Key={"token": token})
        revoked = "Item" in response
        return revoked
