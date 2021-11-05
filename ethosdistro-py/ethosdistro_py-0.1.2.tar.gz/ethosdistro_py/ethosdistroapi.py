from yarl import URL
from aiohttp import (
    ClientSession,
    ClientResponse,
    ClientResponseError,
    ClientConnectionError,
)
from json.decoder import JSONDecodeError
from . import PANEL_ID

from .exceptions import APIError, JsonFormatError, NotFoundError
from .urls import Urls


class EthosAPI(object):
    def __init__(self, session: ClientSession, panel_id: str = PANEL_ID):
        self.__client = session
        self.__panel_id = panel_id
        self.urls = Urls()

    def panel_id_set(self):
        return self.__panel_id is not None

    @staticmethod
    async def __to_json(response: ClientResponse):
        """Private method to call json method on response object

        Parameters
        ----------
        response : ClientResponse
            The response object

        Returns
        -------
        dict
            JSON response represented as a Python dictionary
        """
        return await response.json(content_type="text/html")

    async def __get_data(self, url: URL):
        """Private method to make a GET request to the URL

        Parameters
        ----------
        url : str
            The URL to query

        Returns
        -------
        dict
            JSON response represented as a Python dictionary

        Raises
        ------
        HTTPError
            Raises on HTTP Error
        JSONDecodeError
            Raises when there is an issue parsing the JSON response
        """
        try:
            response = await self.__client.get(url % self.__panel_id)

            # raises if the status code is an error - 4xx, 5xx
            response.raise_for_status()

            return await self.__to_json(response)
        except ClientResponseError as e:
            raise APIError(e)
        except ClientConnectionError as e:
            raise NotFoundError(e)
        except JSONDecodeError as e:
            raise JsonFormatError(e)

    async def async_get_panel(self):
        """Get data show in dashboard panel

        Returns
        -------

        """
        return await self.__get_data(self.urls.get_panel_url(panel_id=self.__panel_id))
