import unittest

from net_models.models import AclStandardIPv4, AclStandardIPv4Entry


from .BaseTemplateTestIos import BaseTemplateTestIos


class TestIosAclStandardIPv4(BaseTemplateTestIos):

    TEMPLATE_NAME = 'ios_acl_standard'
    TEST_CLASS = AclStandardIPv4

    def test_01(self):
        test_cases = [
            {
                "test_name": "Test-01",
                "data": {
                    "params": self.TEST_CLASS(
                        name="ACL-TEST",
                        entries=[
                            AclStandardIPv4Entry(
                                seq_no=10,
                                remark="Test Remark",
                                action="permit",
                                src_address="192.168.0.0/24"
                            ),
                            AclStandardIPv4Entry(
                                seq_no=15,
                                remark="Test Remark 2",
                                action="permit",
                                src_address="10.1.1.1/32"
                            ),
                            AclStandardIPv4Entry(
                                seq_no=20,
                                remark="Test Remark 3",
                                action="deny",
                                src_address="any"
                            ),
                        ]
                    )
                },
                "result": (
                    "ip access-list standard ACL-TEST\n"
                    " 10 remark Test Remark\n"
                    " 10 permit 192.168.0.0 0.0.0.255\n"
                    " 15 remark Test Remark 2\n"
                    " 15 permit 10.1.1.1\n"
                    " 20 remark Test Remark 3\n"
                    " 20 deny   any\n"
                )
            }
        ]
        self.common_testbase(test_cases=test_cases)
