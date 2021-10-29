from typing import Any, Dict, List, Optional

from aiomeilisearch.index import Index
from aiomeilisearch.config import Config
from aiomeilisearch._http_client import HttpClient
from aiomeilisearch.error import AioMeiliSearchError, AioMeiliSearchApiError

class Client():
    """
    A asyncio client for the MeiliSearch API
    A client instance is needed for every MeiliSearch API method to know the location of
    MeiliSearch and its permissions.
    """
    def __init__(
        self, url: str, apiKey: Optional[str] = None, timeout: Optional[int] = None
    ) -> None:
        """
        :param url: url address of MeiliSearch server. example: "http://127.0.0.1:7700"
        :param apiKey: master key
        :param timeout: request timeout
        """
        self.config = Config(url, apiKey, timeout=timeout)
        self.http = HttpClient(self.config)

    def index(self, uid: str) -> Index:
        """
        Create a local reference to an index identified by UID, without doing an HTTP call.
        Calling this method doesn't create an index in the MeiliSearch instance,
        but grants access to all the other methods in the Index class.
        """
        if uid is not None:
            return Index(self.config, uid=uid)
        raise Exception('The index UID should not be None')

    async def get_indexes(self) -> List[Index]:
        """
        List all indexes
        :return:
        """
        indexes = await self.get_raw_indexes()
        return [Index(
                    self.config,
                    index["uid"],
                    index["primaryKey"],
                    index["createdAt"],
                    index["updatedAt"],
                )
                for index in indexes]

    async def get_raw_indexes(self) -> List[Dict[str, Any]]:
        """
        :return: List of indexes in dictionary format. (e.g [{ 'uid': 'movies' 'primaryKey': 'objectID' }])
        """
        path = "/indexes"
        return await self.http.get(path)

    async def get_index(self, uid: str) -> Index:
        """
        Get one index
        :param uid: UID of the index.
        :return: Index Object
        """
        return await Index(self.config, uid).get()

    async def get_raw_index(self, uid: str) -> Dict[str, Any]:
        """Get the index as a dictionary.
        :param uid: UID of the index.
        :return: An index in dictionary format. (e.g { 'uid': 'movies' 'primaryKey': 'objectID' })
        """
        return await Index(self.config, uid).get_raw()

    async def create_index(self, uid: str, options: Optional[Dict[str, Any]] = None) -> Index:
        """
        Create an index
        :param uid: The index unique identifier (mandatory)
        :param options:
            - primaryKey: The primary key of the documents
        :return: Index Object
        """
        path = "/indexes"
        if options:
            json_data = options
        else:
            json_data = {}
        json_data["uid"] = uid
        index_ = await self.http.post(path, json_=json_data)
        return Index(self.config,
                     index_["uid"],
                     index_["primaryKey"],
                     index_["createdAt"],
                     index_["updatedAt"],)

    async def update_index(self, uid: str, options: Optional[Dict[str, Any]] = None) -> Index:
        """
        Update an index.

        :param uid: The index UID, The uid of an index cannot be changed.
        :param options:
            - primaryKey: The primary key of the documents,
                          The primaryKey can be added if it does not exist,
                          if primaryKey already exists, will raise Error
        :return:
        """
        return await Index(self.config, uid).update(**options)

    async def delete_index(self, uid: str) -> None:
        await Index(self.config, uid).delete()

    async def delete_index_if_exists(self, uid: str) -> bool:
        """Deletes an index if it already exists
        :param uid: The index UID, The uid of an index cannot be changed.
        :return: True if an index was deleted or False if not
        """

        try:
            await self.delete_index(uid)
            return True
        except AioMeiliSearchApiError as error:
            if error.error_code != "index_not_found":
                raise error
            return False

    async def get_or_create_index(self, uid: str, options: Optional[Dict[str, Any]] = None) -> Index:
        """
        :param uid: UID of the index
        :param options:
            - primaryKey: The primary key of the documents during index creation
        :return: An instance of Index containing the information of the retrieved or newly created index.
        """
        try:
            index_instance = await self.get_index(uid)
        except AioMeiliSearchApiError as err:
            if err.error_code != 'index_not_found':
                raise err
            index_instance = await self.create_index(uid, options)
        return index_instance

    async def get_all_stats(self) -> Dict[str, Any]:
        """
        Stats
        Get stats of all indexes
        Doc: https://docs.meilisearch.com/reference/api/stats.html
        Stats gives extended information and metrics about indexes and the MeiliSearch database.
        Get information about database size and all indexes
        """
        path = "/stats"
        return await self.http.get(path)

    async def get_index_stats(self, uid) -> Dict[str, Any]:
        """
        Get stats of an index.
        :param uid: UID of the index
        :return: An instance of Index containing the information of the retrieved or newly created index.
        """
        return await Index(self.config, uid).get_stats()

    async def health(self) -> Dict[str, str]:
        """
        Get health of the MeiliSearch server.
        https://docs.meilisearch.com/reference/api/health.html#get-health
        The health check endpoint enables you to periodically test the health of your MeiliSearch instance.
        """
        path = "/health"
        return await self.http.get(path)

    async def is_healthy(self) -> bool:
        """Get health of the MeiliSearch server.
        """
        try:
            await self.health()
        except AioMeiliSearchError:
            return False
        except:
            return False
        return True

    async def get_keys(self) -> Dict[str, str]:
        """
        Get all keys. Get the public and private keys.
        You must have the master key to access the keys route.
        https://docs.meilisearch.com/reference/api/keys.html#get-keys
        """
        path = "/keys"
        return await self.http.get(path)

    async def get_version(self) -> Dict[str, str]:
        """
        Get version of MeiliSearch
        https://docs.meilisearch.com/reference/api/version.html#get-version-of-meilisearch
        :returns: Information about the version of MeiliSearch.
        """
        path = "/version"
        return await self.http.get(path)

    async def version(self) -> Dict[str, str]:
        """Alias for get_version
        """
        return await self.get_version()

    async def create_dump(self) -> Dict[str, str]:
        """
        Trigger the creation of a MeiliSearch dump.
        https://docs.meilisearch.com/reference/api/dump.html#create-a-dump
        :returns: Information about the dump.
        """
        path = "/dumps"
        return await self.http.post(path)

    async def get_dump_status(self, uid: str) -> Dict[str, str]:
        """Get the status of a dump creation process using the uid returned after create_dump().
        :uid: UID of the dump.
        :return:
            Information about the dump status.
            https://docs.meilisearch.com/reference/api/dump.html#get-dump-status
        """
        path = "/dumps/{dump_uid}/status".format(dump_uid=uid)
        return await self.http.get(path)
