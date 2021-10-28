# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class CreatePublishedPipelineRequest(Model):
    """CreatePublishedPipelineRequest.

    :param use_pipeline_endpoint:
    :type use_pipeline_endpoint: bool
    :param pipeline_name:
    :type pipeline_name: str
    :param pipeline_description:
    :type pipeline_description: str
    :param use_existing_pipeline_endpoint:
    :type use_existing_pipeline_endpoint: bool
    :param pipeline_endpoint_name:
    :type pipeline_endpoint_name: str
    :param pipeline_endpoint_description:
    :type pipeline_endpoint_description: str
    :param set_as_default_pipeline_for_endpoint:
    :type set_as_default_pipeline_for_endpoint: bool
    :param step_tags: This is a dictionary
    :type step_tags: dict[str, str]
    :param experiment_name:
    :type experiment_name: str
    :param pipeline_parameters: This is a dictionary
    :type pipeline_parameters: dict[str, str]
    :param data_path_assignments: This is a dictionary
    :type data_path_assignments: dict[str, ~designer.models.LegacyDataPath]
    :param data_set_definition_value_assignments: This is a dictionary
    :type data_set_definition_value_assignments: dict[str,
     ~designer.models.DataSetDefinitionValue]
    :param enable_notification:
    :type enable_notification: bool
    :param sub_pipelines_info:
    :type sub_pipelines_info: ~designer.models.SubPipelinesInfo
    :param display_name:
    :type display_name: str
    :param graph:
    :type graph: ~designer.models.GraphDraftEntity
    :param module_node_run_settings:
    :type module_node_run_settings:
     list[~designer.models.GraphModuleNodeRunSetting]
    :param tags: This is a dictionary
    :type tags: dict[str, str]
    :param continue_run_on_step_failure:
    :type continue_run_on_step_failure: bool
    :param description:
    :type description: str
    :param properties: This is a dictionary
    :type properties: dict[str, str]
    """

    _attribute_map = {
        'use_pipeline_endpoint': {'key': 'usePipelineEndpoint', 'type': 'bool'},
        'pipeline_name': {'key': 'pipelineName', 'type': 'str'},
        'pipeline_description': {'key': 'pipelineDescription', 'type': 'str'},
        'use_existing_pipeline_endpoint': {'key': 'useExistingPipelineEndpoint', 'type': 'bool'},
        'pipeline_endpoint_name': {'key': 'pipelineEndpointName', 'type': 'str'},
        'pipeline_endpoint_description': {'key': 'pipelineEndpointDescription', 'type': 'str'},
        'set_as_default_pipeline_for_endpoint': {'key': 'setAsDefaultPipelineForEndpoint', 'type': 'bool'},
        'step_tags': {'key': 'stepTags', 'type': '{str}'},
        'experiment_name': {'key': 'experimentName', 'type': 'str'},
        'pipeline_parameters': {'key': 'pipelineParameters', 'type': '{str}'},
        'data_path_assignments': {'key': 'dataPathAssignments', 'type': '{LegacyDataPath}'},
        'data_set_definition_value_assignments': {'key': 'dataSetDefinitionValueAssignments', 'type': '{DataSetDefinitionValue}'},
        'enable_notification': {'key': 'enableNotification', 'type': 'bool'},
        'sub_pipelines_info': {'key': 'subPipelinesInfo', 'type': 'SubPipelinesInfo'},
        'display_name': {'key': 'displayName', 'type': 'str'},
        'graph': {'key': 'graph', 'type': 'GraphDraftEntity'},
        'module_node_run_settings': {'key': 'moduleNodeRunSettings', 'type': '[GraphModuleNodeRunSetting]'},
        'tags': {'key': 'tags', 'type': '{str}'},
        'continue_run_on_step_failure': {'key': 'continueRunOnStepFailure', 'type': 'bool'},
        'description': {'key': 'description', 'type': 'str'},
        'properties': {'key': 'properties', 'type': '{str}'},
    }

    def __init__(self, *, use_pipeline_endpoint: bool=None, pipeline_name: str=None, pipeline_description: str=None, use_existing_pipeline_endpoint: bool=None, pipeline_endpoint_name: str=None, pipeline_endpoint_description: str=None, set_as_default_pipeline_for_endpoint: bool=None, step_tags=None, experiment_name: str=None, pipeline_parameters=None, data_path_assignments=None, data_set_definition_value_assignments=None, enable_notification: bool=None, sub_pipelines_info=None, display_name: str=None, graph=None, module_node_run_settings=None, tags=None, continue_run_on_step_failure: bool=None, description: str=None, properties=None, **kwargs) -> None:
        super(CreatePublishedPipelineRequest, self).__init__(**kwargs)
        self.use_pipeline_endpoint = use_pipeline_endpoint
        self.pipeline_name = pipeline_name
        self.pipeline_description = pipeline_description
        self.use_existing_pipeline_endpoint = use_existing_pipeline_endpoint
        self.pipeline_endpoint_name = pipeline_endpoint_name
        self.pipeline_endpoint_description = pipeline_endpoint_description
        self.set_as_default_pipeline_for_endpoint = set_as_default_pipeline_for_endpoint
        self.step_tags = step_tags
        self.experiment_name = experiment_name
        self.pipeline_parameters = pipeline_parameters
        self.data_path_assignments = data_path_assignments
        self.data_set_definition_value_assignments = data_set_definition_value_assignments
        self.enable_notification = enable_notification
        self.sub_pipelines_info = sub_pipelines_info
        self.display_name = display_name
        self.graph = graph
        self.module_node_run_settings = module_node_run_settings
        self.tags = tags
        self.continue_run_on_step_failure = continue_run_on_step_failure
        self.description = description
        self.properties = properties
