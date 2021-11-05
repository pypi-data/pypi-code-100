import typing

from aioalfacrm.core.object_ import AlfaObject


class Subject(AlfaObject):
    object_name = 'subject'

    async def list(
            self,
            page: int = 0,
            count: int = 100,
            name: typing.Optional[str] = None,
            **kwargs,
    ):
        """
        Get list customers
        :param page: page
        :param count: count branches of page
        :param name: filter by name
        :param kwargs: additional filters
        :return: list of branches
        """
        return await self._list(
            page,
            count,
            name=name,
            **kwargs
        )
