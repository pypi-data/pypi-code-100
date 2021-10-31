from typing import Optional

from MSApi.ProductFolder import ProductFolder
from MSApi.MSLowApi import MSLowApi, error_handler, caching


class GenerateListMixin:

    @classmethod
    @caching
    def gen_list(cls, **kwargs):
        return MSLowApi.gen_objects('entity/{}'.format(cls._type_name), cls, **kwargs)
