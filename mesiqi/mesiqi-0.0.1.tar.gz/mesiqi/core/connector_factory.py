"""Factory for creating a connector."""

from typing import Any, Callable, Dict

from mesiqi.core.connector import Connector

connector_creation_funcs: Dict[str, Callable[..., Connector]] = {}


def register(connector_type: str, creator_fn: Callable[..., Connector]) -> None:
    """Register a new connector type."""
    connector_creation_funcs[connector_type] = creator_fn


def unregister(connector_type: str) -> None:
    """Unregister a connector type."""
    connector_creation_funcs.pop(connector_type, None)


def create(arguments: Dict[str, Any]) -> Connector:
    """Create a connector of a specific type."""
    args_copy = arguments.copy()
    connector_type = args_copy.pop("type")
    try:
        creator_func = connector_creation_funcs[connector_type]
    except KeyError:
        raise ValueError(f"unknown connector type {connector_type!r}") from None
    return creator_func(**args_copy)
