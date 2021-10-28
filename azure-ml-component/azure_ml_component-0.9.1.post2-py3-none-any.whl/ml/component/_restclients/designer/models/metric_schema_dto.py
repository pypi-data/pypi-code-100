# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class MetricSchemaDto(Model):
    """MetricSchemaDto.

    :param num_properties:
    :type num_properties: int
    :param properties:
    :type properties: list[~designer.models.MetricSchemaPropertyDto]
    """

    _attribute_map = {
        'num_properties': {'key': 'numProperties', 'type': 'int'},
        'properties': {'key': 'properties', 'type': '[MetricSchemaPropertyDto]'},
    }

    def __init__(self, **kwargs):
        super(MetricSchemaDto, self).__init__(**kwargs)
        self.num_properties = kwargs.get('num_properties', None)
        self.properties = kwargs.get('properties', None)
