from typing import Any, Callable
from uuid import uuid4

from asgi_correlation_id.context import celery_current_id, celery_parent_id, correlation_id


def configure_correlation_ids_for_celery(sentry_extension: Callable, uuid_length: int) -> None:
    """
    Transfer correlation IDs from a HTTP request to a Celery worker,
    when spawned from a request.

    This is called as long as Celery is installed.
    """
    from celery import Task
    from celery.signals import before_task_publish, task_postrun, task_prerun

    header_key = 'CORRELATION_ID'

    @before_task_publish.connect
    def transfer_correlation_id(headers: dict, **kwargs: Any) -> None:
        """
        Transfer correlation ID from request thread to Celery worker, by adding
        it as a header.

        This way we're able to correlate work executed by Celery workers, back
        to the originating request, when there was one.
        """
        headers[header_key] = correlation_id.get()

    @task_prerun.connect
    def load_correlation_id(task: Task, **kwargs: Any) -> None:
        """
        Set correlation ID from header if it exists.

        If it doesn't exist, generate a unique ID for the task anyway.
        """
        id_value = task.request.get(header_key)
        if id_value:
            correlation_id.set(id_value)
            sentry_extension(id_value)
        else:
            generated_correlation_id = uuid4().hex
            correlation_id.set(generated_correlation_id[:uuid_length])
            sentry_extension(generated_correlation_id)

    @task_postrun.connect
    def cleanup(_: Task, **kwargs: Any) -> None:
        """
        Clear context vars, to avoid re-using values in the next task.

        Context vars are cleared automatically in a HTTP request-setting,
        but must be manually reset for workers.
        """
        correlation_id.set(None)


def configure_celery_current_and_parent_id(uuid_length: int = 32) -> None:
    """
    Configure Celery event hooks for generating tracing IDs with depth.

    This is not called automatically by the middleware.
    To use this, users should manually run it during startup.
    """
    from celery import Task
    from celery.signals import before_task_publish, task_postrun, task_prerun

    header_key: str = 'CELERY_PARENT_ID'

    @before_task_publish.connect
    def publish_task_from_worker_or_request(headers: dict, **kwargs: Any) -> None:
        """
        Transfer the current ID to the next Celery worker, by adding
        it as a header.

        This way we're able to tell which process spawned the next task.
        """
        current = celery_current_id.get()
        if current:
            headers[header_key] = current

    @task_prerun.connect
    def worker_prerun(task: Task, **kwargs: Any) -> None:
        """
        Set current ID, and parent ID if it exists.
        """
        parent_id = task.request.get(header_key)
        if parent_id:
            celery_parent_id.set(parent_id)

        current_id = uuid4().hex[:uuid_length]
        celery_current_id.set(current_id)

    @task_postrun.connect
    def clean_up(_: Task, **kwargs: Any) -> None:
        """
        Clear context vars, to avoid re-using values in the next task.
        """
        celery_current_id.set(None)
        celery_parent_id.set(None)
