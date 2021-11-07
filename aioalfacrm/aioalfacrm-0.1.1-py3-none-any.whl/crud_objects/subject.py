import typing

from aioalfacrm.core.object_ import AlfaCRUDObject
from .. import models


class Subject(AlfaCRUDObject):
    object_name = 'subject'

    async def list(
            self,
            page: int = 0,
            count: int = 100,
            name: typing.Optional[str] = None,
            **kwargs,
    ) -> typing.List[models.Subject]:
        """
        Get list customers
        :param page: page
        :param count: count branches of page
        :param name: filter by name
        :param kwargs: additional filters
        :return: list of branches
        """
        raw_result = await self._list(
            page,
            count,
            name=name,
            **kwargs
        )

        return [models.Subject(item.pop('id'), **item) for item in raw_result['items']]

    async def get(self, id_: int) -> models.Subject:
        raw_result = await self._get(id_)

        return models.Subject(raw_result.pop('id'), **raw_result)

    async def save(self, model: models.Subject) -> models.Subject:
        raw_result = await self._save(**model.serialize())
        return models.Subject(raw_result.pop('id'), **raw_result)
