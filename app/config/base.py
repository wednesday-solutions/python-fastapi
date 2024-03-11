from pydantic import BaseSettings


class DBSettings(BaseSettings):
    DB_HOSTNAME: str
    DB_PORT: str
    DB_NAME: str
    DB_USERNAME: str
    DB_PASSWORD: str

    class Config:
        env_file = ".env"


class Settings(BaseSettings):
    SECRET_KEY: str
    REDIS_URL: str
    SLACK_WEBHOOK_URL: str

    class Config:
        env_file = ".env"


db_settings = DBSettings()
settings = Settings()
