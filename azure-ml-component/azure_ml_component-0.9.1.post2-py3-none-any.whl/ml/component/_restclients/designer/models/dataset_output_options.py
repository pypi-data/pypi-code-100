# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class DatasetOutputOptions(Model):
    """DatasetOutputOptions.

    :param source_globs:
    :type source_globs: ~designer.models.GlobsOptions
    :param path_on_datastore:
    :type path_on_datastore: str
    """

    _attribute_map = {
        'source_globs': {'key': 'sourceGlobs', 'type': 'GlobsOptions'},
        'path_on_datastore': {'key': 'pathOnDatastore', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(DatasetOutputOptions, self).__init__(**kwargs)
        self.source_globs = kwargs.get('source_globs', None)
        self.path_on_datastore = kwargs.get('path_on_datastore', None)
