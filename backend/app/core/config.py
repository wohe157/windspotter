from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="WS_", env_file=".env", env_file_encoding="utf-8"
    )

    app_name: str = "Windspotter"
    aws_default_region: str = "eu-west-1"

    auth_secret_key: str
    auth_jwt_algorithm: str = "HS256"
    auth_access_token_expire_minutes: int = 30
    auth_refresh_token_expire_days: int = 30

    dynamodb_users_table: str
    dynamodb_users_index_by_email: str


settings = Settings()
