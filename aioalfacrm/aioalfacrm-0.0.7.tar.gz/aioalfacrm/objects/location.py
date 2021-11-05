import typing

from ..core.object_ import AlfaObject


class Location(AlfaObject):
    object_name = 'location'

    async def list(
            self,
            page: int = 0,
            count: int = 100,
            name: typing.Optional[str] = None,
            is_active: typing.Optional[bool] = None,
            **kwargs,
    ):
        """
        Get list locations
        :param name: filter by name
        :param is_active: filter by is_active
        :param page: page
        :param count: count branches of page
        :param kwargs: additional filters
        :return: list of branches
        """
        return await self._list(page, count, name=name, is_active=is_active, **kwargs)
