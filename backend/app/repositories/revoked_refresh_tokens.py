from app.core.config import settings

from .common import get_table

table = get_table(settings.dynamodb_revoked_refresh_tokens)


def revoke_token(token: str) -> None:
    table.put_item(Item={"token": token})


def token_is_revoked(token: str) -> bool:
    response = table.get_item(Key={"token": token})
    return "Item" in response
