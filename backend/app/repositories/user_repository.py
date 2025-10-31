from datetime import datetime, timedelta, timezone
from uuid import uuid4

from boto3.dynamodb.conditions import Key

from app.core.config import settings
from app.core.exceptions import ItemAlreadyExistsException, ItemNotFoundException
from app.db.database import get_dynamodb_table
from app.models.user import User


class UserRepository:
    def __init__(self):
        self.table = get_dynamodb_table(settings.dynamodb_users_table)

    def get_user_by_id(self, user_id: str) -> User:
        response = self.table.get_item(Key={"user_id": user_id})
        user_data = response.get("Item")
        if user_data is None:
            raise ItemNotFoundException("User does not exist.")
        return User(**user_data)

    def get_user_by_email(self, email: str) -> User:
        response = self.table.query(
            IndexName=settings.dynamodb_users_index_by_email,
            KeyConditionExpression=Key("email").eq(email),
            Limit=1,
        )
        user_data = response.get("Items")
        if len(user_data) != 1:
            raise ItemNotFoundException("Email is not in use.")
        return User(**user_data[0])

    def create_user(
        self, email: str, password_hash: str, name: str | None = None
    ) -> None:
        response = self.table.query(
            IndexName=settings.dynamodb_users_index_by_email,
            KeyConditionExpression=Key("email").eq(email),
            Limit=1,
        )
        if len(response.get("Items")) > 0:
            raise ItemAlreadyExistsException("Email is already in use.")
        user = User(
            user_id=str(uuid4()),
            name=name,
            email=email,
            password_hash=password_hash,
            is_active=True,
        )
        self.table.put_item(Item=user.model_dump())

    def update_user_data(
        self,
        user_id: str,
        name: str | None = None,
        email: str | None = None,
        password_hash: str | None = None,
    ) -> None:
        expressions = []
        values = {}
        attribute_names = {}

        if name is not None:
            expressions.append("#N = :name")
            values[":name"] = name
            attribute_names["#N"] = "name"

        if email is not None:
            expressions.append("email = :email")
            values[":email"] = email

            response = self.table.query(
                IndexName=settings.dynamodb_users_index_by_email,
                KeyConditionExpression=Key("email").eq(email),
                Limit=1,
            )
            if len(response.get("Items")) > 0:
                raise ItemAlreadyExistsException("Email is already in use.")

        if password_hash is not None:
            expressions.append("password_hash = :password_hash")
            values[":password_hash"] = password_hash

        if not expressions:
            return

        self.table.update_item(
            Key={"user_id": user_id},
            UpdateExpression="SET " + ", ".join(expressions),
            ExpressionAttributeNames=attribute_names,
            ExpressionAttributeValues=values,
        )

    def delete_user(self, user_id: str) -> None:
        self.table.update_item(
            Key={"user_id": user_id},
            UpdateExpression="SET is_active = :is_active, expires_at = :expires_at",
            ExpressionAttributeValues={
                ":is_active": False,
                ":expires_at": (
                    datetime.now(timezone.utc) + timedelta(days=30)
                ).isoformat(),
            },
        )
