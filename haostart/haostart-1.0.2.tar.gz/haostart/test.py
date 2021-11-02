from functools import wraps


def logit(func):
    @wraps(func)
    def with_logging(*args, **kwargs):

        print(
            f"\033[34m函数\033[0m\033[33m{func.__name__}\033[0m\033[34m已被调用\033[0m")
        return func(*args, **kwargs)
    return with_logging


@logit
def addition_func(x):

    return x + x


result = addition_func(4)
