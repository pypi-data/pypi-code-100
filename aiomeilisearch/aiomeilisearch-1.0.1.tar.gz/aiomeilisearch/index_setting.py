from typing import Any, Dict, Generator, List, Optional, Union

from aiomeilisearch.config import Config
from aiomeilisearch._http_client import HttpClient

class SettingObject():
    def __init__(self, config: Config, index_uid: str, tail_path: str):
        self.config = config
        self.index_uid = index_uid
        self.http = HttpClient(config)
        self.path = "/indexes/{index_uid}/{tail_path}".format(index_uid=index_uid, tail_path=tail_path)

    async def get(self) -> Dict[str, Any]:
        return await self.http.get(self.path)

    async def update(self, *args, **params) -> Dict[str, int]:
        """
        :return:
            {
              "updateId": 1
            }
        """
        payload = args or params or None
        return await self.http.post(self.path, json_=payload)

    async def reset(self) -> Dict[str, int]:
        """
        :return:
            {
              "updateId": 1
            }
        """
        return await self.http.delete(self.path,)

class Setting(SettingObject):
    """
    https://docs.meilisearch.com/reference/api/settings.html#get-settings
    """
    def __init__(self, config: Config, index_uid: str,) -> None:
        super(Setting, self).__init__(config, index_uid, "settings")

class DisplayedAttribute(SettingObject):
    """
    https://docs.meilisearch.com/reference/api/displayed_attributes.html
    """
    def __init__(self, config: Config, index_uid: str,) -> None:
        super(DisplayedAttribute, self).__init__(config, index_uid, "settings/displayed-attributes")

class DistinctAttribute(SettingObject):
    """
    https://docs.meilisearch.com/reference/api/distinct_attribute.html
    """
    def __init__(self, config: Config, index_uid: str,) -> None:
        super(DistinctAttribute, self).__init__(config, index_uid, "settings/distinct-attribute")

    async def update(self, attribute) -> Dict[str, int]:
        """
        :return:
            {
              "updateId": 1
            }
        """
        return await self.http.post(self.path, json_=attribute)

class FilterableAttribute(SettingObject):
    """
    https://docs.meilisearch.com/reference/api/filterable_attributes.html
    """
    def __init__(self, config: Config, index_uid: str,) -> None:
        super(FilterableAttribute, self).__init__(config, index_uid, "settings/filterable-attributes")

class RankingRule(SettingObject):
    """
    https://docs.meilisearch.com/reference/api/ranking_rules.html
    """
    def __init__(self, config: Config, index_uid: str, ) -> None:
        super(RankingRule, self).__init__(config, index_uid, "settings/ranking-rules")

class SearchableAttribute(SettingObject):
    """
    https://docs.meilisearch.com/reference/api/searchable_attributes.html
    """
    def __init__(self, config: Config, index_uid: str, ) -> None:
        super(SearchableAttribute, self).__init__(config, index_uid, "settings/searchable-attributes")

class SortableAttribute(SettingObject):
    """
    https://docs.meilisearch.com/reference/api/sortable_attributes.html
    """
    def __init__(self, config: Config, index_uid: str, ) -> None:
        super(SortableAttribute, self).__init__(config, index_uid, "settings/sortable-attributes")

class StopWord(SettingObject):
    """
    https://docs.meilisearch.com/reference/api/stop_words.html
    """
    def __init__(self, config: Config, index_uid: str, ) -> None:
        super(StopWord, self).__init__(config, index_uid, "settings/stop-words")

class Synonym(SettingObject):
    """
    https://docs.meilisearch.com/reference/api/synonyms.html
    """
    def __init__(self, config: Config, index_uid: str, ) -> None:
        super(Synonym, self).__init__(config, index_uid, "settings/synonyms")