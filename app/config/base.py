from __future__ import annotations

from pydantic import BaseSettings


class DBSettings(BaseSettings):
    DB_HOSTNAME: str
    DB_PORT: str
    DB_NAME: str
    DB_USERNAME: str
    DB_PASSWORD: str

    class Config:
        env_file = ".env.local"


class Settings(DBSettings):
    SECRET_KEY: str
    REDIS_URL: str
    SENTRY_DSN: str | None
    SLACK_WEBHOOK_URL: str | None
    ALLOWED_HOSTS: list = ["*"]
    CACHE_MAX_AGE: int = 60

    class Config:
        env_file = ".env.local"

    def check_environment_variables(self):
        if not self.DB_HOSTNAME or not self.DB_PORT or not self.DB_NAME or not self.DB_USERNAME or not self.DB_PASSWORD:
            raise ValueError("Database environment variables are not set")

        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY is not set")

        if not self.REDIS_URL:
            raise ValueError("REDIS_URL is not set")


class CachedEndpoints(BaseSettings):
    CACHED_ENDPOINTS: list = ["/cache-sample/"]


class CelerySettings(BaseSettings):
    RESULT_EXPIRES: int
    RESULT_PERSISTENT: bool
    WORKER_SEND_TASK_EVENT: bool
    WORKER_PREFETCH_MULTIPLIER: int

    class Config:
        env_file = ".config.celery"


settings = Settings()
celery_settings = CelerySettings()
cached_endpoints = CachedEndpoints()
