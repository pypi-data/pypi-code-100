import typing

from ..core.object_ import AlfaObject


class Customer(AlfaObject):
    object_name = 'customer'

    async def list(
            self,
            page: int = 0,
            count: int = 100,
            name: typing.Optional[str] = None,
            is_study: typing.Optional[bool] = None,
            legal_type: typing.Optional[int] = None,
            **kwargs,
    ):
        """
        Get list customers
        :param name: filter by name
        :param is_study: filter by is_study
        :param page: page
        :param count: count branches of page
        :param legal_type: client type
        :param kwargs: additional filters
        :return: list of branches
        """
        return await self._list(
            page,
            count,
            name=name,
            is_study=is_study,
            legal_type=legal_type,
            **kwargs)
