import json

from datetime import date, datetime
from typing import Optional, Union

from enderturing import Config
from enderturing.api.api_utils import _to_date_range
from enderturing.http_client import HttpClient


class Raw:
    """Contains methods for raw data access.

    Supported data types:
    - Raw transcripts (as they come from ASR, before postprocessing)
    - Events (e.g. speaker change event, provided by conferencing software)

    Args:
        config (Config): configuration to use.
        client (HttpClient): HTTP client instance to use for requests
    """

    def __init__(self, config: Config, client: HttpClient):
        self._config = config
        self._http_client = client

    def get_transcripts(
        self,
        *,
        skip: int = 0,
        max_results: int = 50,
        from_date: Optional[Union[str, date, datetime]] = None,
        to_date: Optional[Union[str, date, datetime]] = None,
        caller_id: Optional[str] = None,
        language: Optional[str] = None,
        session_id: Optional[str] = None
    ):
        params = {
            "date_range": _to_date_range(from_date, to_date),
            "caller_id": caller_id,
            "language": language,
            "skip": skip,
            "limit": max_results,
            "session_id": session_id,
        }
        return self._http_client.get("/raw/transcripts", params=params)

    def create_transcript(
        self,
        *,
        session_id: str,
        lang_code: str,
        text: Optional[str] = None,
        source: Optional[str] = None,
        caller_id: Optional[str] = None,
        destination_id: Optional[str] = None,
        transcript_data: Optional[Union[dict, str]] = None
    ):
        if text and transcript_data:
            raise ValueError("Parameters `text` and `transcript_data` are mutually exclusive")
        if not text and not transcript_data:
            raise ValueError("One of `text` or `transcript_data` should be not empty")
        if text:
            payload = json.dumps({"text": text}, ensure_ascii=False)
        elif isinstance(transcript_data, dict):
            payload = json.dumps(transcript_data, ensure_ascii=False)
        else:
            payload = transcript_data
        transcript = {
            "payload": payload,
            "source": source,
            "session_id": session_id,
            "caller_id": caller_id,
            "destination_id": destination_id,
            "language_code": lang_code,
        }
        return self._http_client.post("/raw/transcripts", json=[transcript])

    def get_events(
        self,
        *,
        skip: int = 0,
        max_results: int = 50,
        from_date: Union[str, date, datetime] = None,
        to_date: Union[str, date, datetime] = None,
        caller_id: str = None,
        call_id: str = None,
        is_processed: bool = None
    ):
        params = {
            "date_range": _to_date_range(from_date, to_date),
            "caller_id": caller_id,
            "call_id": call_id,
            "skip": skip,
            "limit": max_results,
            "is_processed": is_processed,
        }
        return self._http_client.get("/raw/events", params=params)

    def create_event(
        self,
        call_id: str,
        *,
        event_data: Union[dict, str],
        caller_id: Optional[str] = None,
        source: Optional[str] = None
    ) -> dict:
        payload = json.dumps(event_data, ensure_ascii=False) if isinstance(event_data, dict) else event_data
        event = {
            "call_id": call_id,
            "caller_id": caller_id,
            "payload": payload,
            "source": source,
        }
        return self._http_client.post("/raw/events", json=event)

    def create_cms_event(
        self,
        call_id: str,
        *,
        caller_id: Optional[str] = None,
        participant_id: str,
        participant_name: str,
        active_speaker: bool
    ):
        event_data = {
            "participant_id": participant_id,
            "participant_name": participant_name,
            "active_speaker": active_speaker,
        }
        return self.create_event(call_id, caller_id=caller_id, source="CMS", event_data=event_data)
