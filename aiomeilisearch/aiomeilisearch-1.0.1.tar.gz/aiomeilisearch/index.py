from typing import Any, Dict, Generator, List, Optional, Union

from aiomeilisearch.config import Config
from datetime import datetime
from aiomeilisearch._http_client import HttpClient
from aiomeilisearch.document import Document
from aiomeilisearch.index_setting import Setting, DisplayedAttribute, DistinctAttribute, FilterableAttribute,\
    RankingRule, SearchableAttribute, SortableAttribute, StopWord, Synonym
from aiomeilisearch.error import AioMeiliSearchApiError

class Index():
    """
    https://docs.meilisearch.com/reference/api/indexes.html
    """
    def __init__(self,
                 config: Config,
                 uid: str,
                 primary_key: Optional[str] = None,
                 created_at: Optional[Union[datetime, str]] = None,
                 updated_at: Optional[Union[datetime, str]] = None,
                 ) -> None:
        self.config = config
        self.http = HttpClient(config)
        self.uid = uid
        self.primary_key = primary_key
        self.created_at = self._iso_to_date_time(created_at)
        self.updated_at = self._iso_to_date_time(updated_at)
        # document
        self.document = Document(config=config, index_uid=uid)

    @staticmethod
    def _iso_to_date_time(iso_date: Optional[Union[datetime, str]]) -> Optional[datetime]:
        """
        MeiliSearch returns the date time information in iso format. Python's implementation of
        datetime can only handle up to 6 digits in microseconds, however MeiliSearch sometimes
        returns more digits than this in the micosecond sections so when that happens this method
        reduces the number of microseconds so Python can handle it. If the value passed is either
        None or already in datetime format the original value is returned.
        """
        if not iso_date:
            return None

        if isinstance(iso_date, datetime):
            return iso_date

        try:
            return datetime.strptime(iso_date, "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            split = iso_date.split(".")
            reduce = len(split[1]) - 6
            reduced = f"{split[0]}.{split[1][:-reduce]}Z"
            return datetime.strptime(reduced, "%Y-%m-%dT%H:%M:%S.%fZ")

    async def fetch_info(self) -> 'Index':
        """
        Fetch the info of the index.
        """
        return await self.get()

    async def get_raw(self)-> Dict:
        """
        :return:  An index in dictionary format. (e.g { 'uid': 'movies' 'primaryKey': 'objectID' })
        """
        path = "/indexes/{0}".format(self.uid)
        index_dict = await self.http.get(path)
        return index_dict

    async def get(self)-> 'Index':
        index_dict = await self.get_raw()
        self.primary_key = index_dict['primaryKey']
        self.created_at = self._iso_to_date_time(index_dict['createdAt'])
        self.updated_at = self._iso_to_date_time(index_dict['updatedAt'])
        return self

    async def update(self, primary_key, **options: Optional[Dict[str, Any]]) -> 'Index':
        """
        Update an index.
        :param options:
            - primaryKey: The primary key of the documents,
                          The primaryKey can be added if it does not exist,
                          if primaryKey already exists, will raise Error
        :return:
        """
        path = "/indexes/{0}".format(self.uid)
        payload = options if options else {}
        if primary_key: payload['primaryKey'] = primary_key
        index_dict = await self.http.put(path, json_=payload)
        self.primary_key = index_dict['primaryKey']
        self.created_at = self._iso_to_date_time(index_dict['createdAt'])
        self.updated_at = self._iso_to_date_time(index_dict['updatedAt'])
        return self

    async def delete(self)-> None:
        """
        Delete an index
        :return: None
        """
        path = "/indexes/{0}".format(self.uid)
        await self.http.delete(path)

    async def delete_if_exists(self) -> bool:
        """Deletes the index if it already exists
        Returns True if an index was deleted or False if not
        """
        try:
            await self.delete()
            return True
        except AioMeiliSearchApiError as error:
            if error.error_code != "index_not_found":
                raise error
            return False
        except:
            raise

    # documents handler
    async def get_document(self, document_id: Union[int, str] ) -> Dict:
        return await self.document.get(document_id)

    async def get_documents(self, kwargs) -> List:
        return await self.document.mget(**kwargs)

    async def add_documents(
        self,
        documents: List[Dict[str, Any]],
        primary_key: Optional[str] = None
    ) -> Dict[str, int]:
        return await self.document.add(documents, primary_key)

    async def update_documents(
        self,
        documents: List[Dict[str, Any]],
        primary_key: Optional[str] = None
    ) -> Dict[str, int]:
        return await self.document.update(documents, primary_key)

    async def delete_document(self, document_id: Union[int, str]) -> Dict[str, int]:
        return await self.document.delete(document_id)

    async def delete_documents(self, document_ids: List[Union[int, str]]) -> Dict[str, int]:
        return await self.document.delete_batch(document_ids)

    async def delete_all_documents(self) -> Dict[str, int]:
        return await self.document.delete_all()

    async def search(self, query: str, *args: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        :param query: str
        :param args: To be compatible with official website demo, allow :

                search('Batman', {
                  'facetsDistribution': ['genres'],
                  'attributesToRetrieve': ['overview', 'title']
                })

                search('Batman', facetsDistribution=['genres'], attributesToRetrieve=['overview', 'title'])

        :param kwargs:
        :return:
        """
        if args and len(args) == 1:
            if isinstance(args[0], dict):
                kwargs = args[0]
        return await self.document.search(query, **kwargs)

    async def get_update_status(self, update_id: int) -> Dict[str, Any]:
        """
        Get the status of an update in a given index.

        :param update_id: the result param "updateId" in self.update()/self.add()/self.delete*()
        :return:
        """
        path = "/indexes/{uid}/updates/{update_id}".format(uid=self.uid, update_id=update_id)
        return await self.http.get(path)

    async def get_all_update_status(self)-> List[Dict[str, Any]]:
        path = "/indexes/{uid}/updates".format(uid=self.uid)
        return await self.http.get(path)

    # stats
    async def get_stats(self) -> Dict[str, Any]:
        """
        Get stats of an index.
        :return: An instance of Index containing the information of the retrieved or newly created index.
        """
        path = "/indexes/{0}/stats".format(self.uid)
        return await self.http.get(path)

    # setting
    def settings(self):
        return Setting(config=self.config, index_uid=self.uid)

    async def get_settings(self) -> Dict[str, Any]:
        return await Setting(config=self.config, index_uid=self.uid).get()

    async def update_settings(self, *args, **params) -> Dict[str, int]:
        if args and len(args) == 1:
            if isinstance(args[0], dict):
                params = args[0]
        return await Setting(config=self.config, index_uid=self.uid).update(**params)

    async def reset_settings(self):
        return await Setting(config=self.config, index_uid=self.uid).reset()

    def displayed_attributes(self):
        return DisplayedAttribute(config=self.config, index_uid=self.uid)

    async def get_displayed_attributes(self) -> Dict[str, Any]:
        return await DisplayedAttribute(config=self.config, index_uid=self.uid).get()

    async def update_displayed_attributes(self, *args, **params) -> Dict[str, int]:
        """
        :param args:
            update_displayed_attributes(["attr1", "attr2"])
            update_displayed_attributes("attr1", "attr2")
        :param params:
        :return:
        """
        if args and len(args) == 1:
            if isinstance(args[0], (tuple, list)):
                args = args[0]
        return await DisplayedAttribute(config=self.config, index_uid=self.uid).update(*args, **params)

    async def reset_displayed_attributes(self):
        return await DisplayedAttribute(config=self.config, index_uid=self.uid).reset()

    def distinct_attribute(self):
        return DistinctAttribute(config=self.config, index_uid=self.uid)

    async def get_distinct_attribute(self) -> Dict[str, Any]:
        return await DistinctAttribute(config=self.config, index_uid=self.uid).get()

    async def update_distinct_attribute(self, attribute) -> Dict[str, int]:
        return await DistinctAttribute(config=self.config, index_uid=self.uid).update(attribute)

    async def reset_distinct_attribute(self):
        return await DistinctAttribute(config=self.config, index_uid=self.uid).reset()

    def filterable_attributes(self):
        return FilterableAttribute(config=self.config, index_uid=self.uid)

    async def get_filterable_attributes(self) -> Dict[str, Any]:
        return await FilterableAttribute(config=self.config, index_uid=self.uid).get()

    async def update_filterable_attributes(self, *args, **params) -> Dict[str, int]:
        """
        :param args:
            update_filterable_attributes(["attr1", "attr2"])
            update_filterable_attributes("attr1", "attr2")
        :param params:
        :return:
        """
        if args and len(args) == 1:
            if isinstance(args[0], (tuple, list)):
                args = args[0]
        return await FilterableAttribute(config=self.config, index_uid=self.uid).update(*args, **params)

    async def reset_filterable_attributes(self):
        return await FilterableAttribute(config=self.config, index_uid=self.uid).reset()

    def ranking_rules(self):
        return RankingRule(config=self.config, index_uid=self.uid)

    async def get_ranking_rules(self) -> Dict[str, Any]:
        return await RankingRule(config=self.config, index_uid=self.uid).get()

    async def update_ranking_rules(self, *args, **params) -> Dict[str, int]:
        """
        :param args:
            update_ranking_rules(["attr1", "attr2"])
            update_ranking_rules("attr1", "attr2")
        :param params:
        :return:
        """
        if args and len(args) == 1:
            if isinstance(args[0], (tuple, list)):
                args = args[0]
        return await RankingRule(config=self.config, index_uid=self.uid).update(*args, **params)

    async def reset_ranking_rules(self):
        return await RankingRule(config=self.config, index_uid=self.uid).reset()

    def searchable_attributes(self):
        return SearchableAttribute(config=self.config, index_uid=self.uid)

    async def get_searchable_attributes(self) -> Dict[str, Any]:
        return await SearchableAttribute(config=self.config, index_uid=self.uid).get()

    async def update_searchable_attributes(self, *args, **params) -> Dict[str, int]:
        """
        :param args:
            update_ranking_rules(["attr1", "attr2"])
            update_ranking_rules("attr1", "attr2")
        :param params:
        :return:
        """
        if args and len(args) == 1:
            if isinstance(args[0], (tuple, list)):
                args = args[0]
        return await SearchableAttribute(config=self.config, index_uid=self.uid).update(*args, **params)

    async def reset_searchable_attributes(self):
        return await SearchableAttribute(config=self.config, index_uid=self.uid).reset()

    def sortable_attributes(self):
        return SortableAttribute(config=self.config, index_uid=self.uid)

    async def get_sortable_attributes(self) -> Dict[str, Any]:
        return await SortableAttribute(config=self.config, index_uid=self.uid).get()

    async def update_sortable_attributes(self, *args, **params) -> Dict[str, int]:
        """

        :param args:
            update_sortable_attributes(["attr1", "attr2"])
            update_sortable_attributes("attr1", "attr2")
        :param params:
        :return:
        """
        if args and len(args) == 1:
            if isinstance(args[0], (tuple, list)):
                args = args[0]
        return await SortableAttribute(config=self.config, index_uid=self.uid).update(*args, **params)

    async def reset_sortable_attributes(self):
        return await SortableAttribute(config=self.config, index_uid=self.uid).reset()

    def stop_words(self):
        return StopWord(config=self.config, index_uid=self.uid)

    async def get_stop_words(self) -> Dict[str, Any]:
        return await StopWord(config=self.config, index_uid=self.uid).get()

    async def update_stop_words(self, *args, **params) -> Dict[str, int]:
        """

        :param args:
            update_sortable_attributes(["attr1", "attr2"])
            update_sortable_attributes("attr1", "attr2")
        :param params:
        :return:
        """
        if args and len(args) == 1:
            if isinstance(args[0], (tuple, list)):
                args = args[0]
        return await StopWord(config=self.config, index_uid=self.uid).update(*args, **params)

    async def reset_stop_words(self):
        return await StopWord(config=self.config, index_uid=self.uid).reset()

    def synonyms(self):
        return Synonym(config=self.config, index_uid=self.uid)

    async def get_synonyms(self) -> Dict[str, Any]:
        return await Synonym(config=self.config, index_uid=self.uid).get()

    async def update_synonyms(self, *args, **params) -> Dict[str, int]:
        if args and len(args) == 1:
            if isinstance(args[0], dict):
                params = args[0]
        return await Synonym(config=self.config, index_uid=self.uid).update(**params)

    async def reset_synonyms(self):
        return await Synonym(config=self.config, index_uid=self.uid).reset()

    # setting EOF
