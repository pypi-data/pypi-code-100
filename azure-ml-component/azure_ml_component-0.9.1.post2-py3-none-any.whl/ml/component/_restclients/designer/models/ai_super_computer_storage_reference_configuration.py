# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class AISuperComputerStorageReferenceConfiguration(Model):
    """AISuperComputerStorageReferenceConfiguration.

    :param container_name:
    :type container_name: str
    :param relative_path:
    :type relative_path: str
    """

    _attribute_map = {
        'container_name': {'key': 'containerName', 'type': 'str'},
        'relative_path': {'key': 'relativePath', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(AISuperComputerStorageReferenceConfiguration, self).__init__(**kwargs)
        self.container_name = kwargs.get('container_name', None)
        self.relative_path = kwargs.get('relative_path', None)
