import typing

from ..core.object_ import AlfaObject


class StudyStatus(AlfaObject):
    object_name = 'study-status'

    async def list(
            self,
            page: int = 0,
            count: int = 100,
            name: typing.Optional[str] = None,
            **kwargs,
    ):
        """
        Get list study statuses
        :param name: filter by name
        :param page: page
        :param count: count branches of page
        :param kwargs: additional filters
        :return: list of branches
        """
        return await self._list(
            page,
            count,
            name=name,
            **kwargs
        )
