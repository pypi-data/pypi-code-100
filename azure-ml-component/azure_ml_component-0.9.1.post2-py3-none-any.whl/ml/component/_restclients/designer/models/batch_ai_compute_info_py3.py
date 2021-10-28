# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class BatchAiComputeInfo(Model):
    """BatchAiComputeInfo.

    :param batch_ai_subscription_id:
    :type batch_ai_subscription_id: str
    :param batch_ai_resource_group:
    :type batch_ai_resource_group: str
    :param batch_ai_workspace_name:
    :type batch_ai_workspace_name: str
    :param cluster_name:
    :type cluster_name: str
    :param native_shared_directory:
    :type native_shared_directory: str
    """

    _attribute_map = {
        'batch_ai_subscription_id': {'key': 'batchAiSubscriptionId', 'type': 'str'},
        'batch_ai_resource_group': {'key': 'batchAiResourceGroup', 'type': 'str'},
        'batch_ai_workspace_name': {'key': 'batchAiWorkspaceName', 'type': 'str'},
        'cluster_name': {'key': 'clusterName', 'type': 'str'},
        'native_shared_directory': {'key': 'nativeSharedDirectory', 'type': 'str'},
    }

    def __init__(self, *, batch_ai_subscription_id: str=None, batch_ai_resource_group: str=None, batch_ai_workspace_name: str=None, cluster_name: str=None, native_shared_directory: str=None, **kwargs) -> None:
        super(BatchAiComputeInfo, self).__init__(**kwargs)
        self.batch_ai_subscription_id = batch_ai_subscription_id
        self.batch_ai_resource_group = batch_ai_resource_group
        self.batch_ai_workspace_name = batch_ai_workspace_name
        self.cluster_name = cluster_name
        self.native_shared_directory = native_shared_directory
