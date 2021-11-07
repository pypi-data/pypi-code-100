import typing

from ..core.object_ import AlfaCRUDObject

T = typing.TypeVar('T')


class StudyStatus(AlfaCRUDObject, typing.Generic[T]):
    object_name = 'study-status'

    async def list(
            self,
            page: int = 0,
            count: int = 100,
            name: typing.Optional[str] = None,
            **kwargs,
    ) -> typing.List[T]:
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

        return [self._model_class(id_=item['id'], **item) for item in raw_result['items']]
