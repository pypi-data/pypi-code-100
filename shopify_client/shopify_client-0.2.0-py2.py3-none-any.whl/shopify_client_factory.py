import shopify

from shopify_client.base_client import BaseClient
from shopify_client.billing import BillingClient
from shopify_client.constants import SupportedClient
from shopify_client.versions import BASE_VERSION
from shopify_client.webhooks import WebhookClient


class ShopifyClientFactory:
    CLIENT_MAPPING = {
        SupportedClient.BILLING.value: BillingClient,
        SupportedClient.WEBHOOK.value: WebhookClient
    }

    def __init__(self, shop, access_token, api_version=BASE_VERSION):
        shopify.ShopifyResource.activate_session(shopify.Session(shop, api_version, access_token))

    @property
    def billing(self) -> BillingClient:
        return self.__get_client(SupportedClient.BILLING.value)

    @property
    def webhook(self) -> WebhookClient:
        return self.__get_client(SupportedClient.WEBHOOK.value)

    def __get_client(self, client_name: str) -> BaseClient:
        return self.CLIENT_MAPPING.get(client_name)()
