from datetime import date, datetime
from typing import List, Literal, Optional, TypedDict, Union

from enderturing import Config
from enderturing.api.api_utils import _to_date_range
from enderturing.api.schemas import SearchResponse
from enderturing.http_client import HttpClient


SessionsList = TypedDict(
    "SessionsList",
    {
        "total": int,
        "items": List[dict],
    },
)


class Sessions:
    def __init__(self, config: Config, client: HttpClient):
        """
        Args:
            config (Config): configuration to use.
            client (HttpClient): HTTP client instance to use for requests
        """
        self._config = config
        self._http_client = client

    def get_session(self, session_id: str):
        return self._http_client.get(f"/sessions/{session_id}")

    def list(
        self,
        *,
        skip: int = 0,
        max_results: int = 50,
        from_date: Union[str, datetime, date] = None,
        to_date: Union[str, datetime, date] = None,
        caller_id: str = None,
        language: str = None,
    ) -> SessionsList:
        params = {
            "date_range": _to_date_range(from_date, to_date),
            "caller_id": caller_id,
            "language": language,
            "skip": skip,
            "limit": max_results,
        }
        return self._http_client.get("/sessions", params=params)

    def update(self, session_id: str, session_data: dict):
        return self._http_client.put(f"/sessions/{session_id}", json=session_data)

    def search(
        self,
        search_query: str = "",
        skip: int = 0,
        limit: Optional[int] = 10,
        from_date: Optional[Union[str, date, datetime]] = None,
        to_date: Optional[Union[str, date, datetime]] = None,
        language: Optional[str] = None,
        call_duration: Optional[int] = None,
        call_duration_compare: Optional[Literal["gt", "gte", "lt", "lte"]] = "gte",
        silence_percent: Optional[int] = None,
        silence_percent_compare: Optional[Literal["gt", "gte", "lt", "lte"]] = "gte",
    ) -> SearchResponse:
        """Performs search by sessions.

        Args:
            search_query: Search query to for full-text search. By default majority of words
                are expected to be in session transcript.
                You can use quotes to enforce some words or phrases in exact form.
                Sample query:
                  have a good day
                It can match with "have a bad day" text, since majority of query words are in the text.
                Another example query (quoted):
                  "have a good day"
                Would match only with a text containing the entire phrase.
                You can mix quoted and unquoted parts to get what you want. Also you can have multiple
                quoted parts of a query. E.g.:
                  have a good day "credit card" "pin"
            skip: Number of sessions to skip, used for pagination
            limit: Number of sessions to return
            from_date: Filter sessions by session.start_dt >= date_from
            to_date: Filter sessions by session.start_dt <= date_to
            language: Filter sessions by language
            call_duration: Filter sessions by duration in seconds. Condition is defined by `call_duration_compare` param
            call_duration_compare: Defines how to filter by `call_duration`.
                E.g. if the value is "gt" - only sessions that are longer than `call_duration` would be returned
                Supported values:
                    "gt" - greater than.
                    "gte" - greater or equal
                    "lt" - less than
                    "lte" - less or equal
            silence_percent: Filters sessions by percentage of silence. Allowed values 0-100
                Condition is defined by `silence_percent_compare`
            silence_percent_compare: Defines how to filter by `silence_percent`.
                E.g. if the value is "gt" - only sessions session.silence_percent > silence_percent would be returned.
                Supported values:
                    "gt" - greater than.
                    "gte" - greater or equal
                    "lt" - less than
                    "lte" - less or equal

        Returns:
            Number of matched sessions and requested range of them
        """
        params = {
            "search_query": search_query,
            "skip": skip,
            "limit": limit,
            "date_range": _to_date_range(from_date, to_date),
            "language": language,
            "call_duration": call_duration,
            "call_duration_compare": call_duration_compare,
            "silence_percent": silence_percent,
            "silence_percent_compare": silence_percent_compare,
        }
        return SearchResponse(**self._http_client.get("/sessions/discovery", params=params))
