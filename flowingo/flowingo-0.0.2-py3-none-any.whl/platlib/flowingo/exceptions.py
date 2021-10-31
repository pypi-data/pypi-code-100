
__all__ = (
    'FlowingoWarning',

    'FlowingoError',
    'TaskError', 'PipelineError'
)


class FlowingoWarning(UserWarning):
    """Base class for all Flowingo warnings."""


class FlowingoError(Exception):
    """Base class for all Flowingo errors."""


class TaskError(Exception):
    """Task related errors."""


class PipelineError(Exception):
    """Pipeline errors."""
