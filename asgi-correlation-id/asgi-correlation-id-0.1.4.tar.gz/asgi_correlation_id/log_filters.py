from logging import Filter, LogRecord

from asgi_correlation_id.context import celery_current_id, celery_parent_id
from asgi_correlation_id.middleware import correlation_id


class CorrelationId(Filter):
    def filter(self, record: LogRecord) -> bool:
        """
        Append a 'correlation_id' value to the log-record.
        """
        record.correlation_id = correlation_id.get()  # type: ignore[attr-defined]
        return True


class CeleryTracingIds(Filter):
    def filter(self, record: LogRecord) -> bool:
        """
        Append 'celery_parent_id' and 'celery_current_id' to log-record.

        Celery parent ID is the tracing ID of the process that spawned the
        current process, and celery current is the current process' tracing ID.
        In other words, if a worker sent a task to be executed by the worker pool,
        that celery worker's current tracing ID would become the next task worker's
        parent tracing ID.
        """
        record.celery_parent_id = celery_parent_id.get()  # type: ignore[attr-defined]
        record.celery_current_id = celery_current_id.get()  # type: ignore[attr-defined]
        return True
