from .client import AliCloudClient
from aliyunsdkvpc.request.v20160428.CreateNatGatewayRequest import CreateNatGatewayRequest
from aliyunsdkvpc.request.v20160428.DeleteNatGatewayRequest import DeleteNatGatewayRequest
from aliyunsdkvpc.request.v20160428.ModifyNatGatewaySpecRequest import ModifyNatGatewaySpecRequest
from aliyunsdkvpc.request.v20160428.ModifyNatGatewayAttributeRequest import ModifyNatGatewayAttributeRequest
from aliyunsdkvpc.request.v20160428.DescribeNatGatewaysRequest import DescribeNatGatewaysRequest


class NatClient(AliCloudClient):
    def __init__(self, secret_id, secret_key, region, config):
        super(NatClient, self).__init__(secret_id, secret_key, region, config, 'vpc')

    def create_nat(self, query_params=None, body_params=None):
        return self.do_request(CreateNatGatewayRequest, query_params, body_params)

    def delete_nat(self, query_params=None, body_params=None):
        return self.do_request(DeleteNatGatewayRequest, query_params, body_params)

    def modify_nat_spec(self, query_params=None, body_params=None):
        return self.do_request(ModifyNatGatewaySpecRequest, query_params, body_params)

    def modify_nat_attrs(self, query_params=None, body_params=None):
        return self.do_request(ModifyNatGatewayAttributeRequest, query_params, body_params)

    def describe_nats(self, query_params=None, body_params=None):
        return self.do_request(DescribeNatGatewaysRequest, query_params, body_params)