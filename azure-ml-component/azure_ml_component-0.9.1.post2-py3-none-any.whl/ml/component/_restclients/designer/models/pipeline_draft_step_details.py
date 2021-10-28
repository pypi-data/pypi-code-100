# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class PipelineDraftStepDetails(Model):
    """PipelineDraftStepDetails.

    :param run_id:
    :type run_id: str
    :param target:
    :type target: str
    :param status: Possible values include: 'NotStarted', 'Unapproved',
     'Pausing', 'Paused', 'Starting', 'Preparing', 'Queued', 'Running',
     'Finalizing', 'CancelRequested', 'Completed', 'Failed', 'Canceled'
    :type status: str or ~designer.models.RunStatus
    :param status_detail:
    :type status_detail: str
    :param parent_run_id:
    :type parent_run_id: str
    :param start_time:
    :type start_time: datetime
    :param end_time:
    :type end_time: datetime
    :param is_reused:
    :type is_reused: bool
    :param logs: This is a dictionary
    :type logs: dict[str, str]
    :param output_log:
    :type output_log: str
    :param outputs: This is a dictionary
    :type outputs: dict[str, str]
    :param port_outputs: This is a dictionary
    :type port_outputs: dict[str, ~designer.models.PortOutputInfo]
    :param is_experiment_archived:
    :type is_experiment_archived: bool
    """

    _attribute_map = {
        'run_id': {'key': 'runId', 'type': 'str'},
        'target': {'key': 'target', 'type': 'str'},
        'status': {'key': 'status', 'type': 'str'},
        'status_detail': {'key': 'statusDetail', 'type': 'str'},
        'parent_run_id': {'key': 'parentRunId', 'type': 'str'},
        'start_time': {'key': 'startTime', 'type': 'iso-8601'},
        'end_time': {'key': 'endTime', 'type': 'iso-8601'},
        'is_reused': {'key': 'isReused', 'type': 'bool'},
        'logs': {'key': 'logs', 'type': '{str}'},
        'output_log': {'key': 'outputLog', 'type': 'str'},
        'outputs': {'key': 'outputs', 'type': '{str}'},
        'port_outputs': {'key': 'portOutputs', 'type': '{PortOutputInfo}'},
        'is_experiment_archived': {'key': 'isExperimentArchived', 'type': 'bool'},
    }

    def __init__(self, **kwargs):
        super(PipelineDraftStepDetails, self).__init__(**kwargs)
        self.run_id = kwargs.get('run_id', None)
        self.target = kwargs.get('target', None)
        self.status = kwargs.get('status', None)
        self.status_detail = kwargs.get('status_detail', None)
        self.parent_run_id = kwargs.get('parent_run_id', None)
        self.start_time = kwargs.get('start_time', None)
        self.end_time = kwargs.get('end_time', None)
        self.is_reused = kwargs.get('is_reused', None)
        self.logs = kwargs.get('logs', None)
        self.output_log = kwargs.get('output_log', None)
        self.outputs = kwargs.get('outputs', None)
        self.port_outputs = kwargs.get('port_outputs', None)
        self.is_experiment_archived = kwargs.get('is_experiment_archived', None)
