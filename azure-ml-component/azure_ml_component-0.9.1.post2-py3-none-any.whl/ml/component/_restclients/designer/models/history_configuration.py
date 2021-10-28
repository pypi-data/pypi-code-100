# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class HistoryConfiguration(Model):
    """HistoryConfiguration.

    :param output_collection:  Default value: True .
    :type output_collection: bool
    :param directories_to_watch:
    :type directories_to_watch: list[str]
    :param enable_mlflow_tracking:  Default value: True .
    :type enable_mlflow_tracking: bool
    """

    _attribute_map = {
        'output_collection': {'key': 'outputCollection', 'type': 'bool'},
        'directories_to_watch': {'key': 'directoriesToWatch', 'type': '[str]'},
        'enable_mlflow_tracking': {'key': 'enableMLflowTracking', 'type': 'bool'},
    }

    def __init__(self, **kwargs):
        super(HistoryConfiguration, self).__init__(**kwargs)
        self.output_collection = kwargs.get('output_collection', True)
        self.directories_to_watch = kwargs.get('directories_to_watch', None)
        self.enable_mlflow_tracking = kwargs.get('enable_mlflow_tracking', True)
