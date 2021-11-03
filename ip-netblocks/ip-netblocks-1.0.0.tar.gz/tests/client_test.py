import os
import unittest
from ipnetblocks import Client
from ipnetblocks import ParameterError, ApiAuthError

ips = ['8.8.8.8', '1.1.1.1', '2.2.2.2']
orgs = ['gogl', 'google', 'parkway', 'amphitheatre']
invalid_ip = '345.567.890.12'


class TestClient(unittest.TestCase):
    """
    Final integration tests without mocks.

    Active API_KEY is required.
    """
    def setUp(self) -> None:
        self.client = Client(os.getenv('API_KEY'))

    def test_get_correct_data(self):
        response = self.client.get(ips[0], limit=10)
        self.assertRegex(response.inetnums[0].AS.name.lower(), 'google')

    def test_search_by_asn(self):
        response = self.client.get_by_asn(15169)
        self.assertRegex(response.inetnums[0].AS.name.lower(), 'google')

    def test_search_by_org(self):
        response = self.client.get_by_org(orgs, limit=10)
        self.assertRegex(response.inetnums[0].AS.name.lower(), 'google')

    def test_no_search_terms(self):
        with self.assertRaises(ParameterError):
            self.client.get()

    def test_invalid_domain(self):
        with self.assertRaises(ParameterError):
            self.client.get(invalid_ip)

    def test_incorrect_api_key(self):
        client = Client('at_00000000000000000000000000000')
        with self.assertRaises(ApiAuthError):
            client.get(ips[1])

    def test_raw_data(self):
        response = self.client.get_raw(
            ip=ips[1], output_format=Client.XML_FORMAT)
        self.assertTrue(response.startswith('<?xml'))


if __name__ == '__main__':
    unittest.main()
