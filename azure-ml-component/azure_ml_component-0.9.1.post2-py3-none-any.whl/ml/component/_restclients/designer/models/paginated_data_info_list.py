# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class PaginatedDataInfoList(Model):
    """A paginated list of DataInfos.

    :param value: An array of objects of type DataInfo.
    :type value: list[~designer.models.DataInfo]
    :param continuation_token:
    :type continuation_token: str
    :param next_link:
    :type next_link: str
    """

    _attribute_map = {
        'value': {'key': 'value', 'type': '[DataInfo]'},
        'continuation_token': {'key': 'continuationToken', 'type': 'str'},
        'next_link': {'key': 'nextLink', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(PaginatedDataInfoList, self).__init__(**kwargs)
        self.value = kwargs.get('value', None)
        self.continuation_token = kwargs.get('continuation_token', None)
        self.next_link = kwargs.get('next_link', None)
