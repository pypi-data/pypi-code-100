import json
from dataclasses import dataclass
from typing import List


@dataclass
class TranscribeData:
    """A container class for an actualized insight "payload".

    Constituants:
        title (str): The title of the insight (i.e. High VA Opportunity)
        headline (str): The one word description that describes the insight (i.e. save $6200)
        transcription (dict): The wording of the insight 
    """
    headline: str
    transcription: str


class _TranscribeDataEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, TranscribeData):
            return {"Headline": obj.headline,
                    "Phrase": obj.transcription}
        return json.JSONEncoder.default(self, obj)
