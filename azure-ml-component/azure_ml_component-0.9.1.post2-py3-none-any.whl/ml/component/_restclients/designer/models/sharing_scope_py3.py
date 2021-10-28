# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class SharingScope(Model):
    """SharingScope.

    :param type: Possible values include: 'Global', 'Tenant', 'Subscription',
     'ResourceGroup', 'Workspace'
    :type type: str or ~designer.models.ScopeType
    :param identifier:
    :type identifier: str
    """

    _attribute_map = {
        'type': {'key': 'type', 'type': 'str'},
        'identifier': {'key': 'identifier', 'type': 'str'},
    }

    def __init__(self, *, type=None, identifier: str=None, **kwargs) -> None:
        super(SharingScope, self).__init__(**kwargs)
        self.type = type
        self.identifier = identifier
