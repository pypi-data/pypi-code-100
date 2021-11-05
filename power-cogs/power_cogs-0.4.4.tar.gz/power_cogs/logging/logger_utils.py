from functools import wraps


def safe(f):
    """wrap function with try / catch
    Args:
        f ([type]): function to wrap
    """

    @wraps(f)
    def new_func(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except Exception:
            pass

    return new_func


def doublewrap(f):
    """
    from https://stackoverflow.com/questions/653368/how-to-create-a-python-decorator-that-can-be-used-either-with-or-without-paramet
    answer by @bj0
    a decorator decorator, allowing the decorator to be used as:
    @decorator(with, arguments, and=kwargs)
    or
    @decorator
    """

    @wraps(f)
    def new_dec(*args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            # actual decorated function
            return f(args[0])
        else:
            # decorator arguments
            return lambda realf: f(realf, *args, **kwargs)

    return new_dec
