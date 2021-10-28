# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ExecutionDataPath(Model):
    """ExecutionDataPath.

    :param datastore_name:
    :type datastore_name: str
    :param relative_path:
    :type relative_path: str
    """

    _attribute_map = {
        'datastore_name': {'key': 'datastoreName', 'type': 'str'},
        'relative_path': {'key': 'relativePath', 'type': 'str'},
    }

    def __init__(self, *, datastore_name: str=None, relative_path: str=None, **kwargs) -> None:
        super(ExecutionDataPath, self).__init__(**kwargs)
        self.datastore_name = datastore_name
        self.relative_path = relative_path
