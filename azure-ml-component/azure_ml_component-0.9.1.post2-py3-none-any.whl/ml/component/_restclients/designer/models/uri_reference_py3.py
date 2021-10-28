# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class UriReference(Model):
    """UriReference.

    :param path:
    :type path: str
    :param is_file:
    :type is_file: bool
    """

    _attribute_map = {
        'path': {'key': 'path', 'type': 'str'},
        'is_file': {'key': 'isFile', 'type': 'bool'},
    }

    def __init__(self, *, path: str=None, is_file: bool=None, **kwargs) -> None:
        super(UriReference, self).__init__(**kwargs)
        self.path = path
        self.is_file = is_file
