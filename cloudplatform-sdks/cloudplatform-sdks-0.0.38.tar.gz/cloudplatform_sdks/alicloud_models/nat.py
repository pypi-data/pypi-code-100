from .clients import nat_client


class AliNatDomain:
    def __init__(self, obj):
        self.obj = obj

    @classmethod
    def create(cls, params):
        response = nat_client.create_nat(params)
        return response.get("NatGatewayId")

    @classmethod
    def update_attrs(cls, params):
        nat_client.modify_nat_attrs(params)

    @classmethod
    def update_spec(cls, params):
        nat_client.modify_nat_spec(params)

    @classmethod
    def get_nats(cls, params=None):
        response = nat_client.describe_nats(params)
        return response

    @classmethod
    def delete(cls, params):
        nat_client.delete_nat(params)