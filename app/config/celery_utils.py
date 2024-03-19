from __future__ import annotations

from celery import current_app as current_celery_app
from celery.result import AsyncResult

from .base import celery_settings
from .celery_config import celery_settings as settings


def create_celery():
    celery_app = current_celery_app
    celery_app.config_from_object(settings, namespace="CELERY")
    celery_app.conf.update(task_track_started=True)
    celery_app.conf.update(task_serializer="pickle")
    celery_app.conf.update(result_serializer="pickle")
    celery_app.conf.update(accept_content=["pickle", "json"])
    celery_app.conf.update(result_expires=celery_settings.RESULT_EXPIRES)
    celery_app.conf.update(result_persistent=celery_settings.RESULT_PERSISTENT)
    celery_app.conf.update(worker_send_task_events=celery_settings.WORKER_SEND_TASK_EVENT)
    celery_app.conf.update(worker_prefetch_multiplier=celery_settings.WORKER_PREFETCH_MULTIPLIER)
    return celery_app


def get_task_info(task_id):
    """
    return task info for the given task_id
    """
    task_result = AsyncResult(task_id)
    result = {"task_id": task_id, "task_status": task_result.status, "task_result": task_result.result}
    return result
