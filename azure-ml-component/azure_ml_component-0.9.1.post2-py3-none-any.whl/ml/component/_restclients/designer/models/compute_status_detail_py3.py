# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ComputeStatusDetail(Model):
    """ComputeStatusDetail.

    :param provisioning_state:
    :type provisioning_state: str
    :param provisioning_error_message:
    :type provisioning_error_message: str
    """

    _attribute_map = {
        'provisioning_state': {'key': 'provisioningState', 'type': 'str'},
        'provisioning_error_message': {'key': 'provisioningErrorMessage', 'type': 'str'},
    }

    def __init__(self, *, provisioning_state: str=None, provisioning_error_message: str=None, **kwargs) -> None:
        super(ComputeStatusDetail, self).__init__(**kwargs)
        self.provisioning_state = provisioning_state
        self.provisioning_error_message = provisioning_error_message
