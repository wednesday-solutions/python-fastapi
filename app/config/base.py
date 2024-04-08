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
    SLACK_WEBHOOK_URL: str
    ALLOWED_HOSTS: list = ["*"]
    CACHE_MAX_AGE: int = 60

    class Config:
        env_file = ".env.local"


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
