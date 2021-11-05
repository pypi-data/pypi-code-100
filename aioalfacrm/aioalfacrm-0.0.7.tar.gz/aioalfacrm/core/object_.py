import typing

from .api import ApiClient
from .exceptions import NotFound
from .paginator import Paginator


class BaseAlfaObject:
    """Class for description API object"""
    object_name = None

    def __init__(self, api_client: ApiClient):
        self._api_client = api_client

    async def _list(self, page: int, count: int = 100, **kwargs) -> typing.Dict[str, typing.Any]:
        """
        Get objects list from api
        :param page: number of page
        :param count: count items on page
        :param kwargs: additional filters
        :return: objects list
        """
        list_url = self._api_client.get_url_for_method(self.object_name, 'index')
        payload = {
            'page': page,
            'count': count,
            **kwargs
        }
        result = await self._api_client.request(list_url, json=payload)
        return result

    async def _get(self, id_: int) -> typing.Dict[str, typing.Any]:
        """
        Get one object from api
        :param id_: object id
        :return: object
        """
        get_url = self._api_client.get_url_for_method(self.object_name, 'index')
        result = await self._api_client.request(get_url, params={'id': id_})
        if result['count'] == 0:
            raise NotFound(404, f'{self.object_name} not found')
        return result['items'][0]

    async def _create(self, **kwargs) -> typing.Dict[str, typing.Any]:
        """
        Create object in api
        :param kwargs: fields
        :return: created object
        """
        create_url = self._api_client.get_url_for_method(self.object_name, 'create')
        result = await self._api_client.request(create_url, json=kwargs)
        return result['model']

    async def _update(self, id_: int, **kwargs) -> typing.Dict[str, typing.Any]:
        """
        Update object in api
        :param id_: object id
        :param kwargs: fields
        :return: updated object
        """
        update_url = self._api_client.get_url_for_method(self.object_name, 'update')
        result = await self._api_client.request(update_url, params={'id': id_}, json=kwargs)
        return result['model']


class AlfaObject(BaseAlfaObject):

    async def get(self, id_: int) -> typing.Dict[str, typing.Any]:
        """
        Get branch by id
        :param id_: id
        :return: branch
        """
        return await self._get(id_)

    async def list(
            self,
            page: int = 0,
            count: int = 100,
            **kwargs,
    ) -> typing.Dict[str, typing.Any]:
        """
        Get list branches
        :param page: page
        :param count: count objects on page
        :param kwargs: additional filters
        :return: list of branches
        """
        return await self._list(page, count, **kwargs)

    async def create(
            self,
            fields: typing.Dict[str, typing.Any],
    ) -> typing.Dict[str, typing.Any]:
        return await self._create(**fields)

    async def update(
            self,
            id_: int,
            fields: typing.Dict[str, typing.Any],
    ) -> typing.Dict[str, typing.Any]:
        return await self._update(id_, **fields)

    async def get_paginator(self, start_page: int = 0, page_size: int = 100, **kwargs) -> Paginator[dict]:
        """
        Get page
        :param start_page: start page
        :param page_size: page size
        :return: page
        """
        pagination = Paginator(
            alfa_object=self,
            start_page=start_page,
            page_size=page_size,
            filters=kwargs,
        )

        return pagination
