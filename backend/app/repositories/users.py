import boto3

from app.core.config import settings
from app.models.user import User

from .common import get_table

table = get_table(settings.dynamodb_users_table)


def get_user_by_id(user_id: str) -> User | None:
    response = table.get_item(Key={"user_id": user_id})
    user_data = response.get("Item")
    if user_data is None:
        return None
    return User(**user_data)


def get_user_by_email(email: str) -> User | None:
    response = table.query(
        IndexName=settings.dynamodb_users_index_by_email,
        KeyConditionExpression=boto3.dynamodb.conditions.Key("email").eq(email),
        Limit=1,
    )
    user_data = response.get("Items")
    if len(user_data) != 1:
        return None
    return User(**user_data[0])
