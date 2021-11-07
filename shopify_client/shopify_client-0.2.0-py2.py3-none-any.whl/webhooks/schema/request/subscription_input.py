import dataclasses
from typing import Literal

from shopify_client.webhooks.constants import WebhookSubscriptionFormat


@dataclasses.dataclass
class WebhookSubscriptionInput:
    callback_url: str
    include_fields: [str] = dataclasses.field(default_factory=lambda: [])
    metafield_namespaces: [str] = dataclasses.field(default_factory=lambda: [])
    format: Literal[
        WebhookSubscriptionFormat.JSON.value, WebhookSubscriptionFormat.XML.value
    ] = WebhookSubscriptionFormat.JSON.value
