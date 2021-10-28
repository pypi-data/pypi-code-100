# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class HttpRequestMessage(Model):
    """HttpRequestMessage.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param request_uri:
    :type request_uri: str
    :param version:
    :type version: str
    :param content:
    :type content: ~designer.models.HttpContent
    :param method:
    :type method: ~designer.models.HttpMethod
    :ivar headers:
    :vartype headers: list[~designer.models.KeyValuePairStringIEnumerable1]
    :ivar properties: This is a dictionary
    :vartype properties: dict[str, object]
    """

    _validation = {
        'headers': {'readonly': True},
        'properties': {'readonly': True},
    }

    _attribute_map = {
        'request_uri': {'key': 'requestUri', 'type': 'str'},
        'version': {'key': 'version', 'type': 'str'},
        'content': {'key': 'content', 'type': 'HttpContent'},
        'method': {'key': 'method', 'type': 'HttpMethod'},
        'headers': {'key': 'headers', 'type': '[KeyValuePairStringIEnumerable1]'},
        'properties': {'key': 'properties', 'type': '{object}'},
    }

    def __init__(self, **kwargs):
        super(HttpRequestMessage, self).__init__(**kwargs)
        self.request_uri = kwargs.get('request_uri', None)
        self.version = kwargs.get('version', None)
        self.content = kwargs.get('content', None)
        self.method = kwargs.get('method', None)
        self.headers = None
        self.properties = None
