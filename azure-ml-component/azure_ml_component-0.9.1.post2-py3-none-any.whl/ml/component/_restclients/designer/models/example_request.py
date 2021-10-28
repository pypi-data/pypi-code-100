# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ExampleRequest(Model):
    """ExampleRequest.

    :param inputs: This is a dictionary
    :type inputs: dict[str, list[list[object]]]
    :param global_parameters: This is a dictionary
    :type global_parameters: dict[str, object]
    """

    _attribute_map = {
        'inputs': {'key': 'inputs', 'type': '{[[object]]}'},
        'global_parameters': {'key': 'globalParameters', 'type': '{object}'},
    }

    def __init__(self, **kwargs):
        super(ExampleRequest, self).__init__(**kwargs)
        self.inputs = kwargs.get('inputs', None)
        self.global_parameters = kwargs.get('global_parameters', None)
