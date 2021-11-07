import typing

from .. import models
from ..core.object_ import AlfaCRUDObject


class LeadSource(AlfaCRUDObject):
    object_name = 'lead-source'

    async def list(
            self,
            page: int = 0,
            count: int = 100,
            name: typing.Optional[str] = None,
            code: typing.Optional[str] = None,
            is_enabled: typing.Optional[bool] = None,
            **kwargs,
    ) -> typing.List[models.LeadSource]:
        """
        Get list customers
        :param page: page
        :param count: count branches of page
        :param name: filter by name
        :param code: filter by code
        :param is_enabled: filter by is_enabled
        :param kwargs: additional filters
        :return: list of branches
        """
        raw_result = await self._list(
            page,
            count,
            code=code,
            is_enabled=is_enabled,
            name=name,
            **kwargs
        )
        return [models.LeadSource(raw_result.pop('id'), **raw_result) for item in raw_result['items']]

    async def get(self, id_: int) -> models.LeadSource:
        raw_result = await self._get(id_)
        return models.LeadSource(raw_result.pop('id'), **raw_result)

    async def save(self, model: models.LeadSource) -> models.LeadSource:
        raw_result = await self._save(**model.serialize())
        return models.LeadSource(raw_result.pop('id'), **raw_result)
