"""
    Ory Kratos API

    Documentation for all public and administrative Ory Kratos APIs. Public and administrative APIs are exposed on different ports. Public APIs can face the public internet without any protection while administrative APIs should never be exposed without prior authorization. To protect the administative API port you should use something like Nginx, Ory Oathkeeper, or any other technology capable of authorizing incoming requests.   # noqa: E501

    The version of the OpenAPI document: v0.8.0-alpha.2
    Contact: hi@ory.sh
    Generated by: https://openapi-generator.tech
"""


import sys
import unittest

import ory_kratos_client
from ory_kratos_client.model.submit_self_service_login_flow_with_password_method_body import SubmitSelfServiceLoginFlowWithPasswordMethodBody


class TestSubmitSelfServiceLoginFlowWithPasswordMethodBody(unittest.TestCase):
    """SubmitSelfServiceLoginFlowWithPasswordMethodBody unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSubmitSelfServiceLoginFlowWithPasswordMethodBody(self):
        """Test SubmitSelfServiceLoginFlowWithPasswordMethodBody"""
        # FIXME: construct object with mandatory attributes with example values
        # model = SubmitSelfServiceLoginFlowWithPasswordMethodBody()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
