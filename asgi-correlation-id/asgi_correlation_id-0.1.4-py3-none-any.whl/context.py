from contextvars import ContextVar

full_correlation_id: ContextVar = ContextVar('full_correlation_id', default=None)
correlation_id: ContextVar = ContextVar('correlation_id', default=None)
celery_parent_id: ContextVar = ContextVar('celery_parent', default=None)
celery_current_id: ContextVar = ContextVar('celery_current', default=None)
