import inspect

class Manager(object):

    def __init__(self):
        self.registry = {}

    def register(self, func):
        self.registry[func.__name__] = func
        return func

    def get(self, function_name):
        return self.registry[function_name]

    def get_registry(self):
        return self.registry


manager = Manager()

def register(func):
    return manager.register(func)
    print(manager.registry)

def inject(func):
    def wrap(*args, **kwargs):
        args = list(args)

        signature = inspect.signature(func)
        expected_args = list(signature.parameters)

        registry = manager.get_registry()
        for arg in expected_args:
            if arg in registry:
                function = manager.get(arg)
                args.append(function())

        return func(*args, **kwargs)
    return wrap
