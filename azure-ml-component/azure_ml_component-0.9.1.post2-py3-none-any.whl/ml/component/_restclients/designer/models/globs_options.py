# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class GlobsOptions(Model):
    """GlobsOptions.

    :param glob_patterns:
    :type glob_patterns: list[str]
    """

    _attribute_map = {
        'glob_patterns': {'key': 'globPatterns', 'type': '[str]'},
    }

    def __init__(self, **kwargs):
        super(GlobsOptions, self).__init__(**kwargs)
        self.glob_patterns = kwargs.get('glob_patterns', None)
