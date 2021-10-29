class Endpoint(object):
    # def __init__(self, ...):
    #     ...

    def __call__(self, method: str, *args, **kwargs):
        return getattr(self, method)(*args, **kwargs)
