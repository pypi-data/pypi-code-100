import typing

from .. import models
from ..core.object_ import AlfaCRUDObject


class StudyStatus(AlfaCRUDObject):
    object_name = 'study-status'

    async def list(
            self,
            page: int = 0,
            count: int = 100,
            name: typing.Optional[str] = None,
            **kwargs,
    ) -> typing.List[models.StudyStatus]:
        """
        Get list study statuses
        :param name: filter by name
        :param page: page
        :param count: count branches of page
        :param kwargs: additional filters
        :return: list of branches
        """
        raw_result = await self._list(
            page,
            count,
            name=name,
            **kwargs
        )

        return [models.StudyStatus(item['id'], **item) for item in raw_result['items']]

    async def get(self, id_: int) -> models.StudyStatus:
        raw_result = await self._get(id_)
        return models.StudyStatus(raw_result.pop('id'), **raw_result)

    async def save(self, model: models.StudyStatus) -> models.StudyStatus:
        raw_result = await self._save(**model.serialize())
        return models.StudyStatus(raw_result.pop('id'), **raw_result)
