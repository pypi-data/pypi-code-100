import typing

from .. import models
from ..core.object_ import AlfaCRUDObject


class Location(AlfaCRUDObject):
    object_name = 'location'

    async def list(
            self,
            page: int = 0,
            count: int = 100,
            name: typing.Optional[str] = None,
            is_active: typing.Optional[bool] = None,
            **kwargs,
    ) -> typing.List[models.Location]:
        """
        Get list locations
        :param name: filter by name
        :param is_active: filter by is_active
        :param page: page
        :param count: count branches of page
        :param kwargs: additional filters
        :return: list of branches
        """
        raw_result = await self._list(page, count, name=name, is_active=is_active, **kwargs)

        return [models.Location(item.pop('id'), **item) for item in raw_result['items']]

    async def get(self, id_: int) -> models.Location:
        raw_result = await self._get(id_)

        return models.Location(raw_result.pop('id'), **raw_result)

    async def save(self, model: models.Location) -> models.Location:
        raw_result = await self._save(**model.serialize())

        return models.Location(raw_result.pop('id'), **raw_result)
