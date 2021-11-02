from typing import Optional

from MSApi.ProductFolder import ProductFolder


class ProductfolderMixin:

    def get_productfolder(self) -> Optional[ProductFolder]:
        """Группа"""
        result = self._json.get('productFolder')
        if result is None:
            return None
        return ProductFolder(result)
