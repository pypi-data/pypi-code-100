from typing import Any, Mapping

from vtorch.huggingface.text import TextPairWithMetadata, TextPairWithMetadataExtractor
from vtorch.youscan.defaults import (
    AUTHOR_FIELD,
    AUTHOR_TYPE,
    CHANNEL_FIELD,
    CHANNEL_TYPE,
    IMAGE_URL_FIELD,
    POST_TYPE,
    POST_TYPE_FIELD,
    RESOURCE_TYPE,
    RESOURCE_TYPE_FIELD,
    TEXT,
    TITLE,
    TYPE_FIELD,
)


class TextPairFixedMetadataExtractor(TextPairWithMetadataExtractor):
    def __init__(
        self,
        text_field: str = "text",
        secondary_text_field: str = "title",
        resource_type_feature: bool = False,
        post_type_feature: bool = False,
        image_feature: bool = False,
        author_type_feature: bool = False,
        channel_type_feature: bool = False,
    ):
        self.text_field = text_field
        self.secondary_text_field = secondary_text_field
        self.resource_type_feature = resource_type_feature
        self.post_type_feature = post_type_feature
        self.image_feature = image_feature
        self.author_type_feature = author_type_feature
        self.channel_type_feature = channel_type_feature

    def extract(self, instance: Mapping[str, Any]) -> TextPairWithMetadata:
        def escape(token: str) -> str:
            return f"[{token}]"

        metadata = [
            escape(instance.get(POST_TYPE_FIELD, POST_TYPE)),
            escape(instance.get(RESOURCE_TYPE_FIELD, RESOURCE_TYPE)),
            escape(instance.get(AUTHOR_FIELD, {}).get(TYPE_FIELD, AUTHOR_TYPE)),
            escape(instance.get(CHANNEL_FIELD, {}).get(TYPE_FIELD, CHANNEL_TYPE)),
        ]
        if instance.get(IMAGE_URL_FIELD, None) is not None:
            metadata.append(escape("image"))
        return str(instance.get(self.text_field, TEXT)), str(instance.get(self.secondary_text_field, TITLE)), metadata


class YSMentionCategoricalMetaExtractor(TextPairWithMetadataExtractor):

    POST_TYPE = "post"
    RESOURCE_TYPE = "social"
    UNDEFINED: str = "undefined"
    TEXT = ""
    TITLE = ""

    def extract(self, instance: Mapping[str, Any]) -> TextPairWithMetadata:
        return (
            instance.get("text", self.TEXT),
            instance.get("title", self.TITLE),
            [
                instance.get("postType", self.POST_TYPE),
                instance.get("resourceType", self.RESOURCE_TYPE),
                instance.get("author", {}).get("type", self.UNDEFINED) + "_" + "author",
                instance.get("channel", {}).get("type", self.UNDEFINED) + "_" + "channel",
                "hasImage" if instance.get("imageUrl", instance.get("image_url")) is not None else "",
            ],
        )
