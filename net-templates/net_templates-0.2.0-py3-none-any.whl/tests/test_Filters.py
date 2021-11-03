import ipaddress
import unittest
from net_models.models.BaseModels import BaseNetModel
from net_models.models.interfaces import InterfaceModel
from net_templates.filters import NetFilters
from pydantic.error_wrappers import ValidationError


class TestTemplateFiltersBase(unittest.TestCase):

    pass


class TestFiltersDict(TestTemplateFiltersBase):

    TEST_CLASS = NetFilters()

    def test_filters_dict(self):
        filters = self.TEST_CLASS.filters()
        print(filters)


class TestToVlanRange(TestTemplateFiltersBase):

    TEST_CLASS = NetFilters()

    def test_from_int_list(self):

        test_cases = [
            {
                "test_name": "Test-From-Int-01",
                "data": list(range(1, 4)),
                "result": "1-3"
            },
            {
                "test_name": "Test-From-Int-02",
                "data": [1, 3, 5],
                "result": "1,3,5"
            },
            {
                "test_name": "Test-From-Int-03",
                "data": [1, 2, 3, 4, 5, 7, 8, 9, 11],
                "result": "1-5,7-9,11"
            },
            {
                "test_name": "Test-From-Text-01",
                "data": "all",
                "result": "all"
            },
            {
                "test_name": "Test-From-Text-02",
                "data": "none",
                "result": "none"
            }
        ]
        for test_case in test_cases:
            with self.subTest(msg=test_case["test_name"]):
                want = test_case["result"]
                have = self.TEST_CLASS.to_vlan_range(test_case["data"])
                self.assertEqual(want, have)


class TestToModel(TestTemplateFiltersBase):

    TEST_CLASS = NetFilters()

    def test_valid_01(self):
        data = {
            "name": "Radius-1",
            "server": "192.0.2.1",
            "key": {
                "encryption_type": 0,
                "value": "SuperSecret"
            }
        }
        model = "RadiusServer"
        model_data = self.TEST_CLASS.to_model(data=data, model=model, many=False, serialize=False)
        self.assertIsInstance(model_data, BaseNetModel)

    def test_valid_list_01(self):
        data = [
            {
                "name": "Radius-1",
                "server": "192.0.2.1",
                "key": {
                    "encryption_type": 0,
                    "value": "SuperSecret"
                }
            },
            {
                "name": "Radius-2",
                "server": "192.0.2.2",
                "key": {
                    "encryption_type": 0,
                    "value": "SuperSecret"
                }
            }
        ]
        model = "RadiusServer"
        model_data = self.TEST_CLASS.to_model(data=data, model=model, many=True, serialize=False)
        if not isinstance(model_data, list):
            self.fail("Model data is not list.")
        elif not all([isinstance(x, BaseNetModel) for x in model_data]):
            self.fail("Some elements are not instance of BaseNetModel")

    def test_valid_02(self):
        data = {
            "name": "Radius-1",
            "server": "192.0.2.1",
            "key": {
                "encryption_type": 0,
                "value": "SuperSecret"
            }
        }
        model = "RadiusServer"
        model_data = self.TEST_CLASS.to_model(data=data, model=model, many=False, serialize=True, dict_params={"exclude_none": True})
        self.assertDictEqual(
            model_data,
            {
                'name': 'Radius-1',
                'server': '192.0.2.1',
                'address_version': 'ipv4',
                'key': {
                    'value': 'SuperSecret',
                    'encryption_type': 0
                }
            }
        )

    def test_invalid_01(self):
        data = {
            "name": "Radius-1",
            "server": "192.0.2.1"
        }
        model = "RadiusServer"
        with self.assertRaises(ValidationError):
            model_data = self.TEST_CLASS.to_model(data=data, model=model, many=False, serialize=False)

    def test_invalid_02(self):
        data = {
            "name": "Radius-1",
            "server": "192.0.2.1"
        }
        model = "NonExistentModel"
        with self.assertRaises(ValueError):
            model_data = self.TEST_CLASS.to_model(data=data, model=model, many=False, serialize=False)


class TestValidateData(TestTemplateFiltersBase):

    TEST_CLASS = NetFilters()

    def test_valid_01(self):
        data = {
            "name": "Radius-1",
            "server": "192.0.2.1",
            "key": {
                "encryption_type": 0,
                "value": "SuperSecret"
            }
        }
        model = "RadiusServer"
        self.assertTrue(self.TEST_CLASS.validate_data(data=data, model=model))

    def test_invalid_02(self):
        data = {
            "name": "Radius-1",
            "server": "192.0.2.1"
        }
        model = "RadiusServer"
        self.assertFalse(self.TEST_CLASS.validate_data(data=data, model=model))


class TestIpAddress(TestTemplateFiltersBase):

    TEST_CLASS = NetFilters()
    FILTER = TEST_CLASS.ipaddress

    def test_01(self):
        with self.subTest(msg="Valid Addresses"):
            for test_value in [
                "192.168.0.1",
                "192.168.0.1/24",
                "192.168.0.1/255.255.255.0",
                "192.168.0.0/24",
                "192.168.0.0/255.255.255.0",
                "0.0.0.0/0.0.0.0"
            ]:
                self.assertTrue(self.FILTER(test_value))

        with self.subTest(msg="Invalid Addresses"):
            for test_value in [
                "192.168.0.300",
                "192.168.0.1/33"
            ]:
                self.assertTrue(not self.FILTER(test_value))

        with self.subTest(msg="Get Address from IPv4 Interfaces"):
            for test_value in [
                "192.168.0.1/32",
                "192.168.0.1/24"
            ]:
                want = test_value.split('/')[0]
                have = self.FILTER(test_value, 'address')
                self.assertEqual(want, have)
        with self.subTest(msg="Get Netmask from IPv4 Interfaces"):
            for test_value in [
                "192.168.0.1/32",
                "192.168.0.1/24"
            ]:
                want = str(ipaddress.IPv4Interface(test_value).netmask)
                have = self.FILTER(test_value, 'netmask')
                self.assertEqual(want, have)

        with self.subTest(msg="Get Prefix Length from IPv4 Interfaces"):
            for test_value in [
                "192.168.0.1/32",
                "192.168.0.1/24",
                "192.168.0.0/24"
            ]:
                want = str(ipaddress.IPv4Interface(test_value).network.prefixlen)
                have = self.FILTER(test_value, 'prefixlen')
                self.assertEqual(want, have)


class TestGetVlans(TestTemplateFiltersBase):

    TEST_CLASS = NetFilters()
    FILTER = TEST_CLASS.get_vlans

    def test_get_vlans(self):
        vlan_definitions = [
            {
                "vlan_id": 10,
                "name": "Vlan10",
                "hosts": [
                    {
                        "name": "SW-01"
                    },
                    {
                        "name": "SW-02"
                    }
                ]
            },
            {
                "vlan_id": 11,
                "name": "Vlan11",
                "hosts": [
                    {
                        "name": "SW-01"
                    }
                ]
            },
            {
                "vlan_id": 12,
                "name": "Vlan12",
                "hosts": [
                    {
                        "name": "SW-02"
                    }
                ]
            },
            {
                "vlan_id": 20,
                "name": "Vlan20"
            },

        ]
        with self.subTest(msg="SW-01"):
            want = [
                {
                    "vlan_id": 10,
                    "name": "Vlan10",
                    "hosts": [
                        {
                            "name": "SW-01"
                        },
                        {
                            "name": "SW-02"
                        }
                    ]
                },
                {
                    "vlan_id": 11,
                    "name": "Vlan11",
                    "hosts": [
                        {
                            "name": "SW-01"
                        }
                    ]
                }
            ]
            have = self.FILTER(vlan_definitions=vlan_definitions, host_name="SW-01")
            print(have)
            self.assertEqual(want, have)
        with self.subTest(msg="SW-02"):
            want = [
                {
                    "vlan_id": 10,
                    "name": "Vlan10",
                    "hosts": [
                        {
                            "name": "SW-01"
                        },
                        {
                            "name": "SW-02"
                        }
                    ]
                },
                {
                    "vlan_id": 12,
                    "name": "Vlan12",
                    "hosts": [
                        {
                            "name": "SW-02"
                        }
                    ]
                }
            ]
            have = self.FILTER(vlan_definitions=vlan_definitions, host_name="SW-02")
            print(have)
            self.assertEqual(want, have)


class TestParsePydanticFilter(TestTemplateFiltersBase):

    TEST_CLASS = NetFilters()
    FILTER = TEST_CLASS._parse_pydantic_filter

    def test_01(self):
        interface_data = [
            {
                "name": "Te1/0/1",
                "description": "Test Description",
                "l3_port": {
                    "ipv4": {
                        "addresses": [
                            {
                                "address": "192.0.2.1/30"
                            }
                        ]
                    }
                }
            },
            {
                "name": "Te1/0/2",
                "description": "Test Description",
                "l3_port": {
                    "ipv4": {
                        "addresses": [
                            {
                                "address": "192.0.2.5/30"
                            }
                        ]
                    }
                }
            }
        ]
        data = {
            "include": {"name": '...', "description": '...', "enabled": '...', "l3_port": {"ipv4": ['addresses']}},
            "exclude_none": True
        }
        print(data)
        have = self.FILTER(data=data)
        want = {
            "include": {'name': Ellipsis, 'description': Ellipsis, 'enabled': Ellipsis, 'l3_port': {'ipv4': {'addresses'}}},
            "exclude_none": True
        }
        # data = None
        print(self.TEST_CLASS.to_model(data=interface_data, many=True, model='InterfaceModel', dict_params=data))
        self.assertEqual(want, have)


del TestTemplateFiltersBase

if __name__ == '__main__':
    unittest.main()