# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class DatacacheConfiguration(Model):
    """DatacacheConfiguration.

    :param datacache_id:
    :type datacache_id: str
    :param datacache_store:
    :type datacache_store: str
    :param dataset_id:
    :type dataset_id: str
    :param mode: Possible values include: 'Mount'
    :type mode: str or ~designer.models.DatacacheMode
    :param replica:
    :type replica: int
    :param failure_fallback:
    :type failure_fallback: bool
    :param path_on_compute:
    :type path_on_compute: str
    """

    _attribute_map = {
        'datacache_id': {'key': 'datacacheId', 'type': 'str'},
        'datacache_store': {'key': 'datacacheStore', 'type': 'str'},
        'dataset_id': {'key': 'datasetId', 'type': 'str'},
        'mode': {'key': 'mode', 'type': 'str'},
        'replica': {'key': 'replica', 'type': 'int'},
        'failure_fallback': {'key': 'failureFallback', 'type': 'bool'},
        'path_on_compute': {'key': 'pathOnCompute', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(DatacacheConfiguration, self).__init__(**kwargs)
        self.datacache_id = kwargs.get('datacache_id', None)
        self.datacache_store = kwargs.get('datacache_store', None)
        self.dataset_id = kwargs.get('dataset_id', None)
        self.mode = kwargs.get('mode', None)
        self.replica = kwargs.get('replica', None)
        self.failure_fallback = kwargs.get('failure_fallback', None)
        self.path_on_compute = kwargs.get('path_on_compute', None)
