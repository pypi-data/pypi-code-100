import typing

from .. import models
from ..core.object_ import AlfaCRUDObject


class Branch(AlfaCRUDObject):
    object_name = 'branch'

    async def list(
            self,
            page: int = 0,
            count: int = 100,
            name: typing.Optional[str] = None,
            is_active: typing.Optional[bool] = None,
            subject_ids: typing.Optional[typing.List[int]] = None,
            **kwargs,
    ) -> typing.List[models.Branch]:
        """
        Get list branches
        :param name: filter by name
        :param is_active: filter by is_active
        :param subject_ids: filter by subject_ids
        :param page: page
        :param count: count branches of page
        :param kwargs: additional filters
        :return: list of branches
        """
        row_data = await self._list(page, count, name=name, is_active=is_active, subject_ids=subject_ids, **kwargs)
        return [models.Branch(item.pop('id'), **item) for item in row_data['items']]

    async def get(self, id_: int) -> models.Branch:
        item = await self._get(id_)
        return models.Branch(item.pop('id'), **item)

    async def save(self, branch: models.Branch) -> models.Branch:
        raw_data = await self._save(**branch.serialize())
        return models.Branch(**raw_data)
