import boto3

from app.core.config import settings
from app.db.database import get_dynamodb_table
from app.models.user import User


class UserRepository:
    def __init__(self):
        self.table = get_dynamodb_table(settings.dynamodb_users_table)

    def get_user_by_id(self, user_id: str) -> User | None:
        response = self.table.get_item(Key={"user_id": user_id})
        user_data = response.get("Item")
        if user_data is None:
            return None
        return User(**user_data)

    def get_user_by_email(self, email: str) -> User | None:
        response = self.table.query(
            IndexName=settings.dynamodb_users_index_by_email,
            KeyConditionExpression=boto3.dynamodb.conditions.Key("email").eq(email),
            Limit=1,
        )
        user_data = response.get("Items")
        if len(user_data) != 1:
            return None
        return User(**user_data[0])
