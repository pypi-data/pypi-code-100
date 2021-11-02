from typing import Optional

from MSApi.Assortment import Assortment
from MSApi.mixin import AttributeMixin, SalePricesMixin
from MSApi.mixin import ProductfolderMixin


class Service(Assortment,
              AttributeMixin,
              ProductfolderMixin,
              SalePricesMixin):

    _type_name = 'service'

    def __init__(self, json):
        super().__init__(json)