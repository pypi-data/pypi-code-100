# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class DownloadResourceInfo(Model):
    """DownloadResourceInfo.

    :param download_url:
    :type download_url: str
    :param size:
    :type size: long
    """

    _attribute_map = {
        'download_url': {'key': 'downloadUrl', 'type': 'str'},
        'size': {'key': 'size', 'type': 'long'},
    }

    def __init__(self, **kwargs):
        super(DownloadResourceInfo, self).__init__(**kwargs)
        self.download_url = kwargs.get('download_url', None)
        self.size = kwargs.get('size', None)
