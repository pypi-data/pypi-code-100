# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class SubmitPipelineRunRequest(Model):
    """SubmitPipelineRunRequest.

    :param compute_target:
    :type compute_target: str
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
        'compute_target': {'key': 'computeTarget', 'type': 'str'},
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

    def __init__(self, **kwargs):
        super(SubmitPipelineRunRequest, self).__init__(**kwargs)
        self.compute_target = kwargs.get('compute_target', None)
        self.step_tags = kwargs.get('step_tags', None)
        self.experiment_name = kwargs.get('experiment_name', None)
        self.pipeline_parameters = kwargs.get('pipeline_parameters', None)
        self.data_path_assignments = kwargs.get('data_path_assignments', None)
        self.data_set_definition_value_assignments = kwargs.get('data_set_definition_value_assignments', None)
        self.enable_notification = kwargs.get('enable_notification', None)
        self.sub_pipelines_info = kwargs.get('sub_pipelines_info', None)
        self.display_name = kwargs.get('display_name', None)
        self.graph = kwargs.get('graph', None)
        self.module_node_run_settings = kwargs.get('module_node_run_settings', None)
        self.tags = kwargs.get('tags', None)
        self.continue_run_on_step_failure = kwargs.get('continue_run_on_step_failure', None)
        self.description = kwargs.get('description', None)
        self.properties = kwargs.get('properties', None)
