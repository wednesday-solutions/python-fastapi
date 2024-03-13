from pydantic import BaseSettings


class CelerySettings(BaseSettings):
    RESULT_EXPIRES: int
    RESULT_PERSISTENT: bool
    WORKER_SEND_TASK_EVENT: bool
    WORKER_PREFETCH_MULTIPLIER: int

    class Config:
        env_file = ".config.celery"


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
    ALLOWED_HOSTS: list = ["*"]
    CACHE_MAX_AGE: int = 60

    class Config:
        env_file = ".env"


class CachedEndpoints(BaseSettings):
    CACHED_ENDPOINTS: list = ["/cache-sample/"]


db_settings = DBSettings()
settings = Settings()
celery_settings = CelerySettings()
cached_endpoints = CachedEndpoints()
