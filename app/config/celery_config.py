from __future__ import annotations

from functools import lru_cache

from app.config.base import settings


def route_task(name, args, kwargs, options, task=None, **kw):
    if ":" in name:
        queue, _ = name.split(":")
        return {"queue": queue}
    return {"queue": "celery"}


class BaseConfig:
    CELERY_BROKER_URL: str = f"{settings.REDIS_URL}/6"
    CELERY_RESULT_BACKEND: str = f"{settings.REDIS_URL}/6"
    CELERY_TASK_ROUTES = (route_task,)


@lru_cache
def get_settings():
    config_cls = BaseConfig
    return config_cls()


celery_settings = get_settings()
