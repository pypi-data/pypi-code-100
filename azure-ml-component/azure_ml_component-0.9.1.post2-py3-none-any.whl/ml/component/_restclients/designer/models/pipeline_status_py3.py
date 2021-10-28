# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class PipelineStatus(Model):
    """PipelineStatus.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param status_code: Possible values include: 'NotStarted', 'InDraft',
     'Preparing', 'Running', 'Failed', 'Finished', 'Canceled', 'Throttled',
     'Unknown'
    :type status_code: str or ~designer.models.PipelineStatusCode
    :param run_status: Possible values include: 'NotStarted', 'Unapproved',
     'Pausing', 'Paused', 'Starting', 'Preparing', 'Queued', 'Running',
     'Finalizing', 'CancelRequested', 'Completed', 'Failed', 'Canceled'
    :type run_status: str or ~designer.models.RunStatus
    :param status_detail:
    :type status_detail: str
    :param start_time:
    :type start_time: datetime
    :param end_time:
    :type end_time: datetime
    :ivar is_terminal_state:
    :vartype is_terminal_state: bool
    """

    _validation = {
        'is_terminal_state': {'readonly': True},
    }

    _attribute_map = {
        'status_code': {'key': 'statusCode', 'type': 'str'},
        'run_status': {'key': 'runStatus', 'type': 'str'},
        'status_detail': {'key': 'statusDetail', 'type': 'str'},
        'start_time': {'key': 'startTime', 'type': 'iso-8601'},
        'end_time': {'key': 'endTime', 'type': 'iso-8601'},
        'is_terminal_state': {'key': 'isTerminalState', 'type': 'bool'},
    }

    def __init__(self, *, status_code=None, run_status=None, status_detail: str=None, start_time=None, end_time=None, **kwargs) -> None:
        super(PipelineStatus, self).__init__(**kwargs)
        self.status_code = status_code
        self.run_status = run_status
        self.status_detail = status_detail
        self.start_time = start_time
        self.end_time = end_time
        self.is_terminal_state = None
