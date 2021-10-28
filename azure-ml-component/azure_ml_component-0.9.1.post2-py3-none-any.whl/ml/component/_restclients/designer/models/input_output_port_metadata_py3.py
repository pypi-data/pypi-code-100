# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class InputOutputPortMetadata(Model):
    """InputOutputPortMetadata.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param graph_module_node_id:
    :type graph_module_node_id: str
    :param port_name:
    :type port_name: str
    :param schema:
    :type schema: str
    :param name:
    :type name: str
    :ivar id:
    :vartype id: str
    """

    _validation = {
        'id': {'readonly': True},
    }

    _attribute_map = {
        'graph_module_node_id': {'key': 'graphModuleNodeId', 'type': 'str'},
        'port_name': {'key': 'portName', 'type': 'str'},
        'schema': {'key': 'schema', 'type': 'str'},
        'name': {'key': 'name', 'type': 'str'},
        'id': {'key': 'id', 'type': 'str'},
    }

    def __init__(self, *, graph_module_node_id: str=None, port_name: str=None, schema: str=None, name: str=None, **kwargs) -> None:
        super(InputOutputPortMetadata, self).__init__(**kwargs)
        self.graph_module_node_id = graph_module_node_id
        self.port_name = port_name
        self.schema = schema
        self.name = name
        self.id = None
