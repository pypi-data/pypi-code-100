import typing
import inspect

def get_name(endpoint: typing.Callable) -> str:
    if inspect.isfunction(endpoint) or inspect.isclass(endpoint):
        return endpoint.__name__
        
    return endpoint.__class__.__name__
