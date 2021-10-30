# pylint: skip-file
from .manager import connections


__all__ = []


async def delete(key, using='default', *args, **kwargs):
    """Delete the given `key` from the cache, if it exists."""
    return await connections[using].delete(key, *args, **kwargs)


async def get(key, using='default', *args, **kwargs):
    """Return given `key` from the cache `using`."""
    return await connections[using].get(key, *args, **kwargs)


async def set(key, value, using='default', *args, **kwargs):
    """Set the given `key` to `value`."""
    return await connections[using].set(key, value, *args, **kwargs)
