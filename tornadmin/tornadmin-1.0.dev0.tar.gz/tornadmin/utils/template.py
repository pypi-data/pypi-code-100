"""Useful functions for using in templates"""
from functools import reduce

def get_value(variable):
    """If the variable is a callable, it will be called.
    
    :TODO: If the variable is a date or datetime object, it will
    return formatted result.

    This is useful in templates to avoid having to check
    whether a variable is callable or not.
    """
    if callable(variable):
        return variable()

    return variable


def get_chained_attr(obj, attr):
    """Similar to getattr, but can also do chained lookups
    using double underscores.

    Example:
    
        get_chained_attr(obj, 'foo__bar')
    """
    return reduce(getattr, attr.split('__'), obj)