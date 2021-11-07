import typing

from ..core.object_ import AlfaCRUDObject

T = typing.TypeVar('T')


class Location(AlfaCRUDObject, typing.Generic[T]):
    object_name = 'location'

    async def list(
            self,
            page: int = 0,
            count: int = 100,
            name: typing.Optional[str] = None,
            is_active: typing.Optional[bool] = None,
            **kwargs,
    ) -> typing.List[T]:
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

        return [self._model_class(id_=item.pop('id'), **item) for item in raw_result['items']]
