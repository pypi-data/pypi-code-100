# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class MpiConfiguration(Model):
    """MpiConfiguration.

    :param process_count_per_node:
    :type process_count_per_node: int
    """

    _attribute_map = {
        'process_count_per_node': {'key': 'processCountPerNode', 'type': 'int'},
    }

    def __init__(self, **kwargs):
        super(MpiConfiguration, self).__init__(**kwargs)
        self.process_count_per_node = kwargs.get('process_count_per_node', None)
