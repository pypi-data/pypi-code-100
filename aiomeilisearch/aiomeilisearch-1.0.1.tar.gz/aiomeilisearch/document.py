from typing import Any, Dict, Generator, List, Optional, Union

from aiomeilisearch.config import Config
from aiomeilisearch._http_client import HttpClient

class Document():
    def __init__(self,
                 config: Config,
                 index_uid: str,
                 ) -> None:
        self.config = config
        self.index_uid = index_uid
        self.http = HttpClient(self.config)

    async def get(self, document_id: Union[int, str]) -> Dict:
        """
        Get one document
        """
        path = "/indexes/{index_uid}/documents/{document_id}".format(index_uid=self.index_uid, document_id=document_id)
        return await self.http.get(path)

    async def mget(self, offset: int=0, limit: int=20, attributes_to_retrieve: List=None, **kwargs) -> List:
        """
        Get documents
        """
        path = "/indexes/{index_uid}/documents".format(index_uid = self.index_uid)
        payload = kwargs if kwargs else {}
        if offset:
            payload['offset'] = offset
        if limit:
            payload['limit'] = limit
        if attributes_to_retrieve:
            payload['attributesToRetrieve'] = ','.join(attributes_to_retrieve)
        return await self.http.get(path, args=payload)

    async def add(
            self,
            documents: List[Dict[str, Any]],
            primary_key: Optional[str] = None
    ) -> Dict[str, int]:
        """
        Add a list of documents or replace them if they already exist.
        If the provided index does not exist, it will be created.

        If you send an already existing document (same documentId)
        the whole existing document will be overwritten by the new document.
        Fields previously in the document not present in the new document are removed.
        """
        path = "/indexes/{index_uid}/documents".format(index_uid = self.index_uid) \
            if not primary_key else \
            "/indexes/{index_uid}/documents?primaryKey={primary_key}".format(
                index_uid = self.index_uid, primary_key=primary_key)
        return await self.http.post(path, json_=documents)

    async def update(
        self,
        documents: List[Dict[str, Any]],
        primary_key: Optional[str] = None
    ) -> Dict[str, int]:
        """
        documents: List of documents. Each document should be a dictionary.
        primary_key (optional): The primary-key used in index. Ignored if already set up

        Add a list of documents or update them if they already exist.
        If the provided index does not exist, it will be created.

        If you send an already existing document (same documentId)
        the old document will be only partially updated according to the fields of the new document.
        Thus, any fields not present in the new document are kept and remained unchanged.
        """
        path = "/indexes/{index_uid}/documents".format(index_uid=self.index_uid) \
            if not primary_key else \
            "/indexes/{index_uid}/documents?primaryKey={primary_key}".format(
                index_uid=self.index_uid, primary_key=primary_key)
        return await self.http.put(path, json_=documents)

    async def delete(self, document_id: Union[int, str]) -> Dict[str, int]:
        path = "/indexes/{index_uid}/documents/{document_id}".format(index_uid=self.index_uid, document_id=document_id)
        return await self.http.delete(path)

    async def delete_batch(self, document_ids: List[Union[int, str]]) -> Dict[str, int]:
        path = "/indexes/{index_uid}/documents/delete-batch".format(index_uid=self.index_uid)
        return await self.http.post(path, document_ids)

    async def delete_all(self) -> Dict[str, int]:
        path = "/indexes/{index_uid}/documents".format(index_uid=self.index_uid)
        return await self.http.delete(path)

    async def search(self, query: str, offset: int=0, limit: int=0, filter: Any=None,
                     facets_distribution: List[str]=None, attributes_to_retrieve: List[str]=None,
                     attributes_to_crop: List[str]=None, crop_length: int=0,
                     attributes_to_highlight: List[str]=None, matches: bool=False, sort: List[str]=None,
                     method="POST", **kwargs) -> Dict[str, Any]:
        """
        :param query:
        :param offset:
        :param limit:
        :param filter:
            A very import param.

        :param facets_distribution:
        :param attributes_to_retrieve:
            ex: To get only the "overview" and "title" fields, set attributesToRetrieve to ["overview", "title"].
        :param attributes_to_crop:
        :param crop_length:
        :param attributes_to_highlight:
        :param matches:
        :param sort:
            When using the POST route, sort expects an array of strings:
                "sort": [
                  "price:asc",
                  "author:desc"
                ]
            When using the GET route, sort expects a comma-separated string:
                sort="price:desc,author:asc"
        :param method:
        :param kwargs:
        :return:
        """
        path = "/indexes/{index_uid}/search".format(index_uid=self.index_uid)
        payload = kwargs if kwargs else {}
        payload['q'] = query
        if offset : payload['offset'] = offset
        if limit  : payload['limit']  = limit
        if filter : payload['filter']  = filter
        if facets_distribution: payload['facetsDistribution'] = facets_distribution
        if attributes_to_retrieve: payload['attributesToRetrieve'] = attributes_to_retrieve
        if attributes_to_crop: payload['attributesToCrop'] = attributes_to_crop
        if crop_length: payload['cropLength'] = crop_length
        if attributes_to_highlight: payload['attributesToHighlight'] = attributes_to_highlight
        if matches: payload['matches'] = matches
        if sort: payload['sort'] = sort
        if method == "POST":
            return await self.http.post(path, json_=payload)
        elif method == "GET":
            """
            Search for documents matching a specific query in the given index.
            This route should only be used when no API key is required. 
            If an API key is required, use the POST route instead.
            """
            if 'sort' in payload:
                payload['sort'] = ','.join(payload['sort'])
            return await self.http.get(path, args=payload)

