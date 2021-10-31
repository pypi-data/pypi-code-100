from logging import Filter, LogRecord
from typing import Type

from asgi_correlation_id.context import celery_current_id, celery_parent_id
from asgi_correlation_id.middleware import correlation_id


def correlation_id_filter(uuid_length: int = 32) -> Type[Filter]:
    class CorrelationId(Filter):
        def filter(self, record: LogRecord) -> bool:
            """
            Append a 'correlation_id' value to the log record.
            """
            cid = correlation_id.get()
            record.correlation_id = cid[:uuid_length] if cid else cid  # type: ignore[attr-defined]
            return True

    return CorrelationId


def celery_tracing_id_filter(uuid_length: int = 32) -> Type[Filter]:
    class CeleryTracingIds(Filter):
        def filter(self, record: LogRecord) -> bool:
            """
            Append 'celery_parent_id' and 'celery_current_id' to the log record.

            Celery parent ID is the tracing ID of the process that spawned the
            current process, and celery current is the current process' tracing ID.
            In other words, if a worker sent a task to be executed by the worker pool,
            that celery worker's current tracing ID would become the next task worker's
            parent tracing ID.
            """
            cpid = celery_parent_id.get()
            ccid = celery_current_id.get()
            record.celery_parent_id = cpid[:uuid_length] if cpid else cpid  # type: ignore[attr-defined]
            record.celery_current_id = ccid[:uuid_length] if ccid else ccid  # type: ignore[attr-defined]
            return True

    return CeleryTracingIds
