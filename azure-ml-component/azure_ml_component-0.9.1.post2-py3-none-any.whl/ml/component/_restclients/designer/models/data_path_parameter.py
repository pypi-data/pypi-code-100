# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class DataPathParameter(Model):
    """DataPathParameter.

    :param name:
    :type name: str
    :param documentation:
    :type documentation: str
    :param default_value:
    :type default_value: ~designer.models.LegacyDataPath
    :param is_optional:
    :type is_optional: bool
    :param data_type_id:
    :type data_type_id: str
    """

    _attribute_map = {
        'name': {'key': 'name', 'type': 'str'},
        'documentation': {'key': 'documentation', 'type': 'str'},
        'default_value': {'key': 'defaultValue', 'type': 'LegacyDataPath'},
        'is_optional': {'key': 'isOptional', 'type': 'bool'},
        'data_type_id': {'key': 'dataTypeId', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(DataPathParameter, self).__init__(**kwargs)
        self.name = kwargs.get('name', None)
        self.documentation = kwargs.get('documentation', None)
        self.default_value = kwargs.get('default_value', None)
        self.is_optional = kwargs.get('is_optional', None)
        self.data_type_id = kwargs.get('data_type_id', None)
