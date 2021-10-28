from sentry_sdk import configure_scope


def set_transaction_id(correlation_id: str) -> None:
    """
    Push the correlation ID as Sentry's transaction ID.

    The transaction ID will appear in the Sentry UI and can be used to correlate
    logs to events.
    """
    with configure_scope() as scope:
        scope.set_tag('transaction_id', correlation_id)
