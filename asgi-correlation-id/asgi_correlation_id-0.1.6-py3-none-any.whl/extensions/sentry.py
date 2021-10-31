from typing import Callable

from sentry_sdk import configure_scope


def get_sentry_extension() -> Callable[[str], None]:
    """
    Return set_transaction_id, if the Sentry-sdk is installed.
    """
    try:
        import sentry_sdk  # noqa: F401

        from asgi_correlation_id.extensions.sentry import set_transaction_id

        return set_transaction_id
    except ImportError:
        return lambda correlation_id: None


def set_transaction_id(correlation_id: str) -> None:
    """
    Push the correlation ID as Sentry's transaction ID.

    The transaction ID will appear in the Sentry UI and can be used to correlate
    logs to events.
    """
    with configure_scope() as scope:
        scope.set_tag('transaction_id', correlation_id)
