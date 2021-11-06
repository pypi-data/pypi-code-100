import typing

from .. import models
from ..core.object_ import AlfaCRUDObject


class Customer(AlfaCRUDObject):
    object_name = 'customer'

    async def list(
            self,
            page: int = 0,
            count: int = 100,
            name: typing.Optional[str] = None,
            is_study: typing.Optional[bool] = None,
            legal_type: typing.Optional[int] = None,
            **kwargs,
    ) -> typing.List[models.Customer]:
        """
        Get list customers
        :param name: filter by name
        :param is_study: filter by is_study
        :param page: page
        :param count: count branches of page
        :param legal_type: client type
        :param kwargs: additional filters
        :return: list of branches
        """
        raw_data = await self._list(
            page,
            count,
            name=name,
            is_study=is_study,
            legal_type=legal_type,
            **kwargs)

        return [models.Customer(item.pop('id'), **item) for item in raw_data['items']]

    async def get(self, id_: int) -> models.Customer:
        raw_data = await self._get(id_)
        return models.Customer(raw_data.pop('id'), **raw_data)

    async def save(self, customer: models.Customer) -> models.Customer:
        raw_data = await self._save(**customer.serialize())
        return models.Customer(raw_data.pop('id'), **raw_data)
