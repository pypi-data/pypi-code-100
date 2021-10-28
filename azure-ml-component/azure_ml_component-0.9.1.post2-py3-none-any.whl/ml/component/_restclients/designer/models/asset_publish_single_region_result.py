# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class AssetPublishSingleRegionResult(Model):
    """AssetPublishSingleRegionResult.

    :param step_name:
    :type step_name: str
    :param status:
    :type status: str
    :param error_message:
    :type error_message: str
    :param last_updated_time:
    :type last_updated_time: datetime
    :param total_steps:
    :type total_steps: int
    :param finished_steps:
    :type finished_steps: int
    :param remaining_steps:
    :type remaining_steps: int
    """

    _attribute_map = {
        'step_name': {'key': 'stepName', 'type': 'str'},
        'status': {'key': 'status', 'type': 'str'},
        'error_message': {'key': 'errorMessage', 'type': 'str'},
        'last_updated_time': {'key': 'lastUpdatedTime', 'type': 'iso-8601'},
        'total_steps': {'key': 'totalSteps', 'type': 'int'},
        'finished_steps': {'key': 'finishedSteps', 'type': 'int'},
        'remaining_steps': {'key': 'remainingSteps', 'type': 'int'},
    }

    def __init__(self, **kwargs):
        super(AssetPublishSingleRegionResult, self).__init__(**kwargs)
        self.step_name = kwargs.get('step_name', None)
        self.status = kwargs.get('status', None)
        self.error_message = kwargs.get('error_message', None)
        self.last_updated_time = kwargs.get('last_updated_time', None)
        self.total_steps = kwargs.get('total_steps', None)
        self.finished_steps = kwargs.get('finished_steps', None)
        self.remaining_steps = kwargs.get('remaining_steps', None)
