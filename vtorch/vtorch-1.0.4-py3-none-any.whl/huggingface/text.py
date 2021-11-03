from typing import Any, Iterable, Mapping, Tuple

TextPairWithMetadata = Tuple[str, str, Iterable[str]]


class TextPairWithMetadataExtractor(object):
    def extract(self, instance: Mapping[str, Any]) -> TextPairWithMetadata:
        raise NotImplementedError()


class TextExtractor(TextPairWithMetadataExtractor):
    def __init__(self, text_field: str = "text"):
        self.text_field = text_field

    def extract(self, instance: Mapping[str, Any]) -> TextPairWithMetadata:
        return str(instance.get(self.text_field, "")), "", []


class TextPairExtractor(TextPairWithMetadataExtractor):
    def __init__(self, text_field: str = "text", secondary_text_field: str = "title"):
        self.secondary_text_field = secondary_text_field
        self.text_field = text_field

    def extract(self, instance: Mapping[str, Any]) -> TextPairWithMetadata:
        return str(instance.get(self.text_field, "")), str(instance.get(self.secondary_text_field, "")), []
