from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Windspotter API"

    class Config:
        env_file = ".env"


settings = Settings()
