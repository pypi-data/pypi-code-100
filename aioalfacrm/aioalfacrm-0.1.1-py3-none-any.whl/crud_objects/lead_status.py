import typing

from .. import models
from ..core.object_ import AlfaCRUDObject


class LeadStatus(AlfaCRUDObject):
    object_name = 'lead-status'

    async def list(
            self,
            page: int = 0,
            count: int = 100,
            name: typing.Optional[str] = None,
            is_enabled: typing.Optional[bool] = None,
            **kwargs,
    ) -> typing.List[models.LeadStatus]:
        """
        Get list lead statuses
        :param name: filter by name
        :param count: count branches of page
        :param page: page
        :param is_enabled: filter by is_enabled
        :param kwargs: additional filters
        :return: list of branches
        """
        raw_result = await self._list(
            page,
            count,
            name=name,
            is_enabled=is_enabled,
            **kwargs
        )

        return [models.LeadStatus(item.pop('id'), **item) for item in raw_result['items']]

    async def get(self, id_: int) -> models.LeadStatus:
        raw_result = await self._get(id_)
        return models.LeadStatus(raw_result.pop('id'), **raw_result)

    async def save(self, model: models.LeadStatus) -> models.LeadStatus:
        raw_result = await self._save(**model.serialize())
        return models.LeadStatus(raw_result.pop('id'), **raw_result)
