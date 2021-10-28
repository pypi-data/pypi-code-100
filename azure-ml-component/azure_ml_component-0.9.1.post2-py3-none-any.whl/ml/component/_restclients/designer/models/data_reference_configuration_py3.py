# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class DataReferenceConfiguration(Model):
    """DataReferenceConfiguration.

    :param data_store_name:
    :type data_store_name: str
    :param mode: Possible values include: 'Mount', 'Download', 'Upload'
    :type mode: str or ~designer.models.ExecutionDataStoreMode
    :param path_on_data_store:
    :type path_on_data_store: str
    :param path_on_compute:
    :type path_on_compute: str
    :param overwrite:
    :type overwrite: bool
    """

    _attribute_map = {
        'data_store_name': {'key': 'dataStoreName', 'type': 'str'},
        'mode': {'key': 'mode', 'type': 'str'},
        'path_on_data_store': {'key': 'pathOnDataStore', 'type': 'str'},
        'path_on_compute': {'key': 'pathOnCompute', 'type': 'str'},
        'overwrite': {'key': 'overwrite', 'type': 'bool'},
    }

    def __init__(self, *, data_store_name: str=None, mode=None, path_on_data_store: str=None, path_on_compute: str=None, overwrite: bool=None, **kwargs) -> None:
        super(DataReferenceConfiguration, self).__init__(**kwargs)
        self.data_store_name = data_store_name
        self.mode = mode
        self.path_on_data_store = path_on_data_store
        self.path_on_compute = path_on_compute
        self.overwrite = overwrite
