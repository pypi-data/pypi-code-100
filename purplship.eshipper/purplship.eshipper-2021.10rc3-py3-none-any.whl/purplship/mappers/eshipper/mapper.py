from typing import List, Tuple
from purplship.api.mapper import Mapper as BaseMapper
from purplship.mappers.eshipper.settings import Settings
from purplship.core.utils.serializable import Deserializable, Serializable
from purplship.core.models import (
    RateRequest,
    ShipmentRequest,
    ShipmentDetails,
    ShipmentCancelRequest,
    RateDetails,
    Message,
    ConfirmationDetails,
)
from purplship.providers.eshipper import (
    parse_quote_reply,
    quote_request,
    parse_shipping_reply,
    shipping_request,
    shipment_cancel_request,
    parse_shipment_cancel_reply,
)


class Mapper(BaseMapper):
    settings: Settings

    # Request Mappers

    def create_rate_request(self, payload: RateRequest) -> Serializable:
        return quote_request(payload, self.settings)

    def create_shipment_request(
        self, payload: ShipmentRequest
    ) -> Serializable:
        return shipping_request(payload, self.settings)

    def create_cancel_shipment_request(self, payload: ShipmentCancelRequest) -> Serializable:
        return shipment_cancel_request(payload, self.settings)

    # Response Parsers

    def parse_rate_response(
        self, response: Deserializable[str]
    ) -> Tuple[List[RateDetails], List[Message]]:
        return parse_quote_reply(response.deserialize(), self.settings)

    def parse_shipment_response(
        self, response: Deserializable[str]
    ) -> Tuple[ShipmentDetails, List[Message]]:
        return parse_shipping_reply(response.deserialize(), self.settings)

    def parse_cancel_shipment_response(
        self, response: Deserializable[str]
    ) -> Tuple[ConfirmationDetails, List[Message]]:
        return parse_shipment_cancel_reply(response.deserialize(), self.settings)
