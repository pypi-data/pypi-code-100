from typing import Optional

from MSApi.Assortment import Assortment
from MSApi.ObjectMS import check_init
from MSApi.ProductFolder import ProductFolder
from MSApi.mixin import AttributeMixin, SalePricesMixin


class Bundle(Assortment, AttributeMixin, SalePricesMixin):

    _type_name = 'bundle'

    def __init__(self, json):
        super().__init__(json)

    @check_init
    def get_productfolder(self) -> Optional[ProductFolder]:
        result = self._json.get('productFolder')
        if result is None:
            return None
        return ProductFolder(result)
