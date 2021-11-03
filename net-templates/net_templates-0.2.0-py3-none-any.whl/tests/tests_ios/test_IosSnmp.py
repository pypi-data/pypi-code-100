import unittest
from tests.tests_ios.BaseTemplateTestIos import BaseTemplateTestIos
from net_models.models.services.ServerModels import (
    SnmpUser, SnmpUserAuth, SnmpUserPriv,
    SnmpGroup
)

class TestIosSnmpGroup(BaseTemplateTestIos):

    TEST_CLASS = SnmpGroup
    TEMPLATE_NAME = 'ios_snmp_group'

    def test_01(self):
        test_cases = [
            {
                "test_name": "Test-01",
                "data": {
                    "params": SnmpGroup(
                        name="GroupABC",
                        version='v3',
                        level='priv',
                        read='READ-View',
                        write='WRITE-View',
                        notify='NOTIFY-View',
                    )
                },
                "result": (
                    "snmp-server group GroupABC v3 priv read READ-View write WRITE-View notify NOTIFY-View\n"
                )
            }
        ]
        super().common_testbase(test_cases=test_cases)



class TestIosSnmpUser(BaseTemplateTestIos):

    TEST_CLASS = SnmpUser
    TEMPLATE_NAME = 'ios_snmp_user'

    def test_01(self):
        test_cases = [
            {
                "test_name": "Test-01",
                "data": {
                    "params": SnmpUser(
                        name="User123",
                        group="GroupABC",
                        version='v3',
                        auth=SnmpUserAuth(
                            method='md5',
                            value="AuthPassword123"
                        ),
                        priv=SnmpUserPriv(
                            method='aes',
                            key_length=128,
                            value="PrivPassword123"
                        )
                    )
                },
                "result": (
                    "snmp-server user User123 GroupABC v3 auth md5 AuthPassword123 priv aes 128 PrivPassword123\n"
                )
            }
        ]
        super().common_testbase(test_cases=test_cases)




del BaseTemplateTestIos

if __name__ == '__main__':
    unittest.main()