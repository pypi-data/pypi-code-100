# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class GraphLayout(Model):
    """GraphLayout.

    :param node_layouts: This is a dictionary
    :type node_layouts: dict[str, ~designer.models.NodeLayout]
    :param id:
    :type id: str
    :param etag:
    :type etag: str
    :param created_date:
    :type created_date: datetime
    :param last_modified_date:
    :type last_modified_date: datetime
    """

    _attribute_map = {
        'node_layouts': {'key': 'nodeLayouts', 'type': '{NodeLayout}'},
        'id': {'key': 'id', 'type': 'str'},
        'etag': {'key': 'etag', 'type': 'str'},
        'created_date': {'key': 'createdDate', 'type': 'iso-8601'},
        'last_modified_date': {'key': 'lastModifiedDate', 'type': 'iso-8601'},
    }

    def __init__(self, *, node_layouts=None, id: str=None, etag: str=None, created_date=None, last_modified_date=None, **kwargs) -> None:
        super(GraphLayout, self).__init__(**kwargs)
        self.node_layouts = node_layouts
        self.id = id
        self.etag = etag
        self.created_date = created_date
        self.last_modified_date = last_modified_date
