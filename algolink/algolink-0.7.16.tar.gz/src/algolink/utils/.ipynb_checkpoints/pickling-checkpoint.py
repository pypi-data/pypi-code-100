import dill

dill._dill._reverse_typemap['ClassType'] = type


class AlgoLinkPickler(dill.Pickler):
    """Base class for `pickle` serializers in AlgoLink. Based on `dill` library."""
    pass


class AlgoLinkUnpickler(dill.Unpickler):
    """Base class for `pickle` deserializers in AlgoLink. Based on `dill` library."""
    pass
