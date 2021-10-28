from typing import Any, List, Tuple, Dict, Union
from abc import ABC, abstractmethod
from elasticsearch import Elasticsearch
from urllib.parse import urlparse
from tqdm.auto import tqdm
import pandas as pd
import logging
import math
import csv

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.StreamHandler())
LOGGER.setLevel("WARNING")


class Query(ABC):
    @property
    @abstractmethod
    def query(self) -> dict:
        ...


class BoolQuery(Query):
    """Elasticsearch bool query constructor"""

    def __init__(
        self,
        must: Union[List[str], None] = None,
        should: Union[List[str], None] = None,
        must_not: Union[List[str], None] = None,
        filter_: Union[List[str], None] = None,
    ) -> None:
        self._must = must or []
        self._should = should or []
        self._must_not = must_not or []
        self._filter = filter_ or []

    @property
    def query(self) -> dict:
        return {
            "_source": [],
            "query": {
                "bool": {
                    "must": self._must,
                    "should": self._should,
                    "must_not": self._must_not,
                    "filter": self._filter,
                }
            },
        }


class UrlQuery(Query):
    """Elasticsearch url query constructor"""

    def __init__(self, url: str) -> None:
        self._url = self._parse_url(url)

    def _parse_url(self, url: str) -> str:
        try:
            parsed_url = urlparse(url)
            parsed_url = (
                "*" + ".".join(parsed_url.hostname.split(".")[-2:]) + parsed_url.path
            )
            return parsed_url.replace("/", r"\/")
        except Exception:
            LOGGER.warning(
                f"Unable to parse url '{url}' with urlparse. Returning raw url."
            )
            return url

    @property
    def query(self) -> dict:
        return {
            "_source": [],
            "query": {
                "query_string": {
                    "fields": [
                        "url.keyword",
                        "secondarySources.url.keyword",
                    ],
                    "query": self._url,
                    "analyzer": "keyword",
                }
            },
        }


class StrQuery(Query):
    """Elasticsearch str query constructor"""

    def __init__(self, field: str, str_: str) -> None:
        self._field = field
        self._str = str_

    @property
    def query(self) -> dict:
        return {"query": {"match_phrase": {self._field: self._str}}}


class Client:
    def __init__(self, host: str, **elasticsearch_kwargs) -> None:
        self._es = Elasticsearch(host, **elasticsearch_kwargs)

    @staticmethod
    def _squeeze(input: List[dict], mapping: Dict[str, Tuple[str]]) -> List[dict]:
        """
        Squeeze list of dict, extract values

        :param input: list of nested dicts
        :param mapping: dict mapping new field names to their paths in nested dicts
        """

        def get_nested(dict_: Union[dict, List[dict]], path: Tuple[str]) -> Any:
            for x in path[:-1]:
                if isinstance(dict_, dict):
                    dict_ = dict_.get(x, {})
                else:
                    dict_ = [y.get(x, {}) for y in dict_]

            if isinstance(dict_, dict):
                return dict_.get(path[-1], None)
            else:
                return [y.get(path[-1], None) for y in dict_]

        return [{y: get_nested(x, mapping[y]) for y in mapping.keys()} for x in input]

    def query(
        self,
        query: Union[Query, dict],
        index: str,
        mapping: Dict[str, Tuple[str]],
        filename: str = "buffer.csv",
        scroll_size: Union[int, None] = 10_000,
        max_scrolls: Union[int, None] = None,
        verbose: int = 0,
        return_=False,
    ) -> Union[pd.DataFrame, None]:
        """
        Run query at index, write list of squeezed dicts to json file

        :param query: query to run
        :param index: index to run query at
        :param mapping: dict of field names and field paths to extract from
        :param filename: filename to write output to
        :param scroll_size: size of scroll. Defaults to 10_000
        :param max_scrolls: maximum number of scrolls
        :param verbose: if > 0 show tqdm progress bar
        :param return_: if True return pd.DataFrame
        """
        scroll_size = scroll_size or 10_000

        if isinstance(query, Query):
            query = query.query

        query["_source"] = [".".join(x) for x in mapping.values()]
        result = self._es.search(index=index, scroll="1m", body=query, size=scroll_size)

        scroll_id = result["_scroll_id"]
        total = (
            math.ceil(result["hits"]["total"] / scroll_size)
            if max_scrolls is None
            else min(result["hits"]["total"], max_scrolls)
        )

        with open(filename, "w", newline="") as file:
            writer = csv.DictWriter(file, mapping.keys())
            writer.writeheader()

            for _ in tqdm(
                range(total),
                total=total,
                bar_format="{l_bar}{bar:50}{r_bar}{bar:-10b}",
                colour="blue",
                disable=verbose == 0,
            ):
                results = self._squeeze(
                    [x["_source"] for x in result["hits"]["hits"]] or [{}],
                    mapping=mapping,
                )
                try:
                    result = self._es.scroll(scroll_id=scroll_id, scroll="1m")
                except Exception:
                    LOGGER.warning(
                        "Error while getting next scroll. Finishing preemptively"
                    )
                    break
                scroll_id = result["_scroll_id"]
                writer.writerows(results)

        if return_:
            return pd.read_csv(filename)

    def count_query(self, query: dict, index: str) -> int:
        """
        Return number of hits

        :param query: query to run
        :param index: index to run query at
        """
        try:
            return self._es.search(index=index, body=query)["hits"]["total"]
        except Exception:
            LOGGER.warning(
                "Got an exception while executing query at index. Returning -1."
            )
            return -1
