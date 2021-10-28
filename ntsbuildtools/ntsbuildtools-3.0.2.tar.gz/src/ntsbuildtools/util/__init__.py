"""util/__init__.py -- Utility package for the buildtools project.
This file includes any function definitions that should be available via 'buildtools.util.METHOD_NAME()'.
"""

def is_nonempty_str(obj):
    return isinstance(obj, str) and len(obj) > 0


def hasattr_nonempty_str(obj, attribute):
    return hasattr(obj, attribute) and is_nonempty_str(getattr(obj, attribute))
