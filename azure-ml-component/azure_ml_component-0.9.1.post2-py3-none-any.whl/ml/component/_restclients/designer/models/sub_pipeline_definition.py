# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class SubPipelineDefinition(Model):
    """SubPipelineDefinition.

    :param name:
    :type name: str
    :param description:
    :type description: str
    :param default_compute_target:
    :type default_compute_target: ~designer.models.ComputeSetting
    :param default_data_store:
    :type default_data_store: ~designer.models.DatastoreSetting
    :param pipeline_function_name:
    :type pipeline_function_name: str
    :param id:
    :type id: str
    :param parent_definition_id:
    :type parent_definition_id: str
    :param from_module_name:
    :type from_module_name: str
    :param parameter_list:
    :type parameter_list: list[~designer.models.Kwarg]
    """

    _attribute_map = {
        'name': {'key': 'name', 'type': 'str'},
        'description': {'key': 'description', 'type': 'str'},
        'default_compute_target': {'key': 'defaultComputeTarget', 'type': 'ComputeSetting'},
        'default_data_store': {'key': 'defaultDataStore', 'type': 'DatastoreSetting'},
        'pipeline_function_name': {'key': 'pipelineFunctionName', 'type': 'str'},
        'id': {'key': 'id', 'type': 'str'},
        'parent_definition_id': {'key': 'parentDefinitionId', 'type': 'str'},
        'from_module_name': {'key': 'fromModuleName', 'type': 'str'},
        'parameter_list': {'key': 'parameterList', 'type': '[Kwarg]'},
    }

    def __init__(self, **kwargs):
        super(SubPipelineDefinition, self).__init__(**kwargs)
        self.name = kwargs.get('name', None)
        self.description = kwargs.get('description', None)
        self.default_compute_target = kwargs.get('default_compute_target', None)
        self.default_data_store = kwargs.get('default_data_store', None)
        self.pipeline_function_name = kwargs.get('pipeline_function_name', None)
        self.id = kwargs.get('id', None)
        self.parent_definition_id = kwargs.get('parent_definition_id', None)
        self.from_module_name = kwargs.get('from_module_name', None)
        self.parameter_list = kwargs.get('parameter_list', None)
