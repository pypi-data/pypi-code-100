import circle
from circle.resources.abstract import CreateableAPIResource


class MockWirePayment(CreateableAPIResource):
    OBJECT_NAME = "mocks.payments.wire"

    @classmethod
    def create(cls, *args, **kwargs):
        if circle.api_base != "https://api-sandbox.circle.com":
            raise Exception(
                "Cannot create a mock wire payment in a non-sandbox environment."
            )
        super().create(*args, **kwargs)
