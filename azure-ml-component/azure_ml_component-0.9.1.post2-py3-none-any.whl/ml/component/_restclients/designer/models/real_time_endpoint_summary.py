# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class RealTimeEndpointSummary(Model):
    """RealTimeEndpointSummary.

    :param name:
    :type name: str
    :param description:
    :type description: str
    :param id:
    :type id: str
    :param created_time:
    :type created_time: datetime
    :param updated_time:
    :type updated_time: datetime
    :param compute_type: Possible values include: 'ACI', 'AKS', 'AMLCOMPUTE',
     'IOT', 'AKSENDPOINT', 'MIRSINGLEMODEL', 'MIRAMLCOMPUTE', 'MIRGA',
     'AMLARC', 'BATCHAMLCOMPUTE', 'UNKNOWN'
    :type compute_type: str or ~designer.models.ComputeEnvironmentType
    :param compute_name:
    :type compute_name: str
    :param updated_by:
    :type updated_by: str
    """

    _attribute_map = {
        'name': {'key': 'name', 'type': 'str'},
        'description': {'key': 'description', 'type': 'str'},
        'id': {'key': 'id', 'type': 'str'},
        'created_time': {'key': 'createdTime', 'type': 'iso-8601'},
        'updated_time': {'key': 'updatedTime', 'type': 'iso-8601'},
        'compute_type': {'key': 'computeType', 'type': 'str'},
        'compute_name': {'key': 'computeName', 'type': 'str'},
        'updated_by': {'key': 'updatedBy', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(RealTimeEndpointSummary, self).__init__(**kwargs)
        self.name = kwargs.get('name', None)
        self.description = kwargs.get('description', None)
        self.id = kwargs.get('id', None)
        self.created_time = kwargs.get('created_time', None)
        self.updated_time = kwargs.get('updated_time', None)
        self.compute_type = kwargs.get('compute_type', None)
        self.compute_name = kwargs.get('compute_name', None)
        self.updated_by = kwargs.get('updated_by', None)
