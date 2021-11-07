import typing

from ..core.object_ import AlfaCRUDObject

T = typing.TypeVar('T')


class LeadStatus(AlfaCRUDObject, typing.Generic[T]):
    object_name = 'lead-status'

    async def list(
            self,
            page: int = 0,
            count: int = 100,
            name: typing.Optional[str] = None,
            is_enabled: typing.Optional[bool] = None,
            **kwargs,
    ) -> typing.List[T]:
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

        return [self._model_class(id_=item.pop('id'), **item) for item in raw_result['items']]
