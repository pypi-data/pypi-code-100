# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class GraphReferenceNode(Model):
    """GraphReferenceNode.

    :param graph_id:
    :type graph_id: str
    :param default_compute:
    :type default_compute: ~designer.models.ComputeSetting
    :param default_datastore:
    :type default_datastore: ~designer.models.DatastoreSetting
    :param id:
    :type id: str
    :param module_id:
    :type module_id: str
    :param comment:
    :type comment: str
    :param name:
    :type name: str
    :param module_parameters:
    :type module_parameters: list[~designer.models.ParameterAssignment]
    :param module_metadata_parameters:
    :type module_metadata_parameters:
     list[~designer.models.ParameterAssignment]
    :param module_output_settings:
    :type module_output_settings: list[~designer.models.OutputSetting]
    :param module_input_settings:
    :type module_input_settings: list[~designer.models.InputSetting]
    :param use_graph_default_compute:
    :type use_graph_default_compute: bool
    :param use_graph_default_datastore:
    :type use_graph_default_datastore: bool
    :param regenerate_output:
    :type regenerate_output: bool
    :param control_inputs:
    :type control_inputs: list[~designer.models.ControlInput]
    """

    _attribute_map = {
        'graph_id': {'key': 'graphId', 'type': 'str'},
        'default_compute': {'key': 'defaultCompute', 'type': 'ComputeSetting'},
        'default_datastore': {'key': 'defaultDatastore', 'type': 'DatastoreSetting'},
        'id': {'key': 'id', 'type': 'str'},
        'module_id': {'key': 'moduleId', 'type': 'str'},
        'comment': {'key': 'comment', 'type': 'str'},
        'name': {'key': 'name', 'type': 'str'},
        'module_parameters': {'key': 'moduleParameters', 'type': '[ParameterAssignment]'},
        'module_metadata_parameters': {'key': 'moduleMetadataParameters', 'type': '[ParameterAssignment]'},
        'module_output_settings': {'key': 'moduleOutputSettings', 'type': '[OutputSetting]'},
        'module_input_settings': {'key': 'moduleInputSettings', 'type': '[InputSetting]'},
        'use_graph_default_compute': {'key': 'useGraphDefaultCompute', 'type': 'bool'},
        'use_graph_default_datastore': {'key': 'useGraphDefaultDatastore', 'type': 'bool'},
        'regenerate_output': {'key': 'regenerateOutput', 'type': 'bool'},
        'control_inputs': {'key': 'controlInputs', 'type': '[ControlInput]'},
    }

    def __init__(self, *, graph_id: str=None, default_compute=None, default_datastore=None, id: str=None, module_id: str=None, comment: str=None, name: str=None, module_parameters=None, module_metadata_parameters=None, module_output_settings=None, module_input_settings=None, use_graph_default_compute: bool=None, use_graph_default_datastore: bool=None, regenerate_output: bool=None, control_inputs=None, **kwargs) -> None:
        super(GraphReferenceNode, self).__init__(**kwargs)
        self.graph_id = graph_id
        self.default_compute = default_compute
        self.default_datastore = default_datastore
        self.id = id
        self.module_id = module_id
        self.comment = comment
        self.name = name
        self.module_parameters = module_parameters
        self.module_metadata_parameters = module_metadata_parameters
        self.module_output_settings = module_output_settings
        self.module_input_settings = module_input_settings
        self.use_graph_default_compute = use_graph_default_compute
        self.use_graph_default_datastore = use_graph_default_datastore
        self.regenerate_output = regenerate_output
        self.control_inputs = control_inputs
