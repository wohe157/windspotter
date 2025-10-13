import boto3

from app.core.config import settings


def get_dynamodb_table(table_name: str):
    dynamodb = boto3.resource("dynamodb", region_name=settings.aws_default_region)
    return dynamodb.Table(table_name)
