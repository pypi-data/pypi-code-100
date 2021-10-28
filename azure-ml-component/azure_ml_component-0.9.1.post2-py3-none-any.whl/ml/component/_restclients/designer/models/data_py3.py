# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class Data(Model):
    """Data.

    :param data_location:
    :type data_location: ~designer.models.ExecutionDataLocation
    :param mechanism: Possible values include: 'Direct', 'Mount', 'Download',
     'Hdfs'
    :type mechanism: str or ~designer.models.DeliveryMechanism
    :param environment_variable_name:
    :type environment_variable_name: str
    :param path_on_compute:
    :type path_on_compute: str
    :param overwrite:
    :type overwrite: bool
    :param options:
    :type options: dict[str, str]
    """

    _attribute_map = {
        'data_location': {'key': 'dataLocation', 'type': 'ExecutionDataLocation'},
        'mechanism': {'key': 'mechanism', 'type': 'str'},
        'environment_variable_name': {'key': 'environmentVariableName', 'type': 'str'},
        'path_on_compute': {'key': 'pathOnCompute', 'type': 'str'},
        'overwrite': {'key': 'overwrite', 'type': 'bool'},
        'options': {'key': 'options', 'type': '{str}'},
    }

    def __init__(self, *, data_location=None, mechanism=None, environment_variable_name: str=None, path_on_compute: str=None, overwrite: bool=None, options=None, **kwargs) -> None:
        super(Data, self).__init__(**kwargs)
        self.data_location = data_location
        self.mechanism = mechanism
        self.environment_variable_name = environment_variable_name
        self.path_on_compute = path_on_compute
        self.overwrite = overwrite
        self.options = options
