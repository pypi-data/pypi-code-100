# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class WebServicePort(Model):
    """WebServicePort.

    :param node_id:
    :type node_id: str
    :param port_name:
    :type port_name: str
    :param name:
    :type name: str
    """

    _attribute_map = {
        'node_id': {'key': 'nodeId', 'type': 'str'},
        'port_name': {'key': 'portName', 'type': 'str'},
        'name': {'key': 'name', 'type': 'str'},
    }

    def __init__(self, *, node_id: str=None, port_name: str=None, name: str=None, **kwargs) -> None:
        super(WebServicePort, self).__init__(**kwargs)
        self.node_id = node_id
        self.port_name = port_name
        self.name = name
