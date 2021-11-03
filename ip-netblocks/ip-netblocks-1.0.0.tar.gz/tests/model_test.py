import json
import unittest
from json import loads
from ipnetblocks import Response, ErrorMessage

_json_response_ok = r'''{
    "search": "1.1.1.1",
    "result": {
        "count": 3,
        "limit": 100,
        "inetnums": [
            {
                "inetnum": "1.1.1.0 - 1.1.1.255",
                "inetnumFirst": 281470698586368,
                "inetnumLast": 281470698586623,
                "inetnumFirstString": "281470698586368",
                "inetnumLastString": "281470698586623",
                "as": {
                    "asn": 13335,
                    "name": "Cloudflare",
                    "type": "Content",
                    "route": "1.1.1.0/24",
                    "domain": "https://www.cloudflare.com"
                },
                "netname": "APNIC-LABS",
                "nethandle": "",
                "description": [
                    "APNIC and Cloudflare DNS Resolver project",
                    "Routed globally by AS13335/Cloudflare",
                    "Research prefix for APNIC Labs"
                ],
                "modified": "2020-07-15T13:10:57Z",
                "country": "AU",
                "city": "",
                "address": [],
                "abuseContact": [
                    {
                        "id": "AA1412-AP",
                        "role": "ABUSE APNICRANDNETAU",
                        "email": "helpdesk@apnic.net",
                        "phone": "+000000000",
                        "country": "ZZ",
                        "city": "",
                        "address": [
                            "PO Box 3646",
                            "South Brisbane, QLD 4101",
                            "Australia"
                        ]
                    }
                ],
                "adminContact": [
                    {
                        "id": "AR302-AP",
                        "role": "APNIC RESEARCH",
                        "email": "research@apnic.net",
                        "phone": "+61-7-3858-3188",
                        "country": "AU",
                        "city": "",
                        "address": [
                            "PO Box 3646",
                            "South Brisbane, QLD 4101",
                            "Australia"
                        ]
                    }
                ],
                "techContact": [
                    {
                        "id": "AR302-AP",
                        "role": "APNIC RESEARCH",
                        "email": "research@apnic.net",
                        "phone": "+61-7-3858-3188",
                        "country": "AU",
                        "city": "",
                        "address": [
                            "PO Box 3646",
                            "South Brisbane, QLD 4101",
                            "Australia"
                        ]
                    }
                ],
                "org": {
                    "org": "ORG-ARAD1-AP",
                    "name": "APNIC Research and Development",
                    "email": "helpdesk@apnic.net",
                    "phone": "+61-7-38583100",
                    "country": "AU",
                    "city": "",
                    "postalCode": "",
                    "address": [
                        "6 Cordelia St"
                    ]
                },
                "mntBy": [
                    {
                        "mntner": "APNIC-HM",
                        "email": "helpdesk@apnic.net\nnetops@apnic.net"
                    }
                ],
                "mntDomains": [],
                "mntLower": [],
                "mntRoutes": [
                    {
                        "mntner": "MAINT-AU-APNIC-GM85-AP",
                        "email": "ggm@apnic.net\nggm@pobox.com"
                    }
                ],
                "remarks": [
                    "---------------",
                    "All Cloudflare abuse reporting can be done via",
                    "resolver-abuse@cloudflare.com",
                    "---------------"
                ],
                "source": "APNIC"
            },
            {
                "inetnum": "1.0.0.0 - 1.255.255.255",
                "inetnumFirst": 281470698520576,
                "inetnumLast": 281470715297791,
                "inetnumFirstString": "281470698520576",
                "inetnumLastString": "281470715297791",
                "as": null,
                "netname": "APNIC-AP",
                "nethandle": "",
                "description": [
                    "Asia Pacific Network Information Centre",
                    "Regional Internet Registry for the Asia-Pacific Region",
                    "6 Cordelia Street",
                    "PO Box 3646",
                    "South Brisbane, QLD 4101",
                    "Australia"
                ],
                "modified": "2018-06-13T04:29:35Z",
                "country": "AU",
                "city": "",
                "address": [],
                "abuseContact": [],
                "adminContact": [
                    {
                        "id": "HM20-AP",
                        "role": "APNIC Hostmaster",
                        "email": "helpdesk@apnic.net",
                        "phone": "+61 7 3858 3100",
                        "country": "AU",
                        "city": "",
                        "address": [
                            "6 Cordelia Street",
                            "South Brisbane",
                            "QLD 4101"
                        ]
                    }
                ],
                "techContact": [
                    {
                        "id": "NO4-AP",
                        "person": "APNIC Network Operations",
                        "email": "netops@apnic.net",
                        "phone": "+61 7 3858 3100",
                        "country": "AU",
                        "city": "",
                        "address": [
                            "6 Cordelia Street",
                            "South Brisbane",
                            "QLD 4101"
                        ]
                    }
                ],
                "org": null,
                "mntBy": [
                    {
                        "mntner": "APNIC-HM",
                        "email": "helpdesk@apnic.net\nnetops@apnic.net"
                    }
                ],
                "mntDomains": [],
                "mntLower": [
                    {
                        "mntner": "APNIC-HM",
                        "email": "helpdesk@apnic.net\nnetops@apnic.net"
                    }
                ],
                "mntRoutes": [],
                "remarks": [],
                "source": "APNIC"
            },
            {
                "inetnum": "0.0.0.0 - 1.178.223.255",
                "inetnumFirst": 281470681743360,
                "inetnumLast": 281470710243327,
                "inetnumFirstString": "281470681743360",
                "inetnumLastString": "281470710243327",
                "as": null,
                "netname": "NON-RIPE-NCC-MANAGED-ADDRESS-BLOCK",
                "nethandle": "",
                "description": [
                    "IPv4 address block not managed by the RIPE NCC"
                ],
                "modified": "2020-12-16T15:13:13Z",
                "country": "EU",
                "city": "",
                "address": [],
                "abuseContact": [],
                "adminContact": [],
                "techContact": [],
                "org": null,
                "mntBy": [
                    {
                        "mntner": "RIPE-NCC-HM-MNT",
                        "email": ""
                    }
                ],
                "mntDomains": [],
                "mntLower": [],
                "mntRoutes": [],
                "remarks": [
                    "------------------------------------------------------",
                    "",
                    "For registration information,",
                    "you can consult the following sources:",
                    "",
                    "IANA",
                    "http://www.iana.org/assignments/ipv4-address-space",
                    "http://www.iana.org/assignments/iana-ipv4-special-registry",
                    "http://www.iana.org/assignments/ipv4-recovered-address-space",
                    "",
                    "AFRINIC (Africa)",
                    "http://www.afrinic.net/ whois.afrinic.net",
                    "",
                    "APNIC (Asia Pacific)",
                    "http://www.apnic.net/ whois.apnic.net",
                    "",
                    "ARIN (Northern America)",
                    "http://www.arin.net/ whois.arin.net",
                    "",
                    "LACNIC (Latin America and the Carribean)",
                    "http://www.lacnic.net/ whois.lacnic.net",
                    "",
                    "------------------------------------------------------",
                    "****************************",
                    "* THIS OBJECT IS MODIFIED",
                    "* Please note that all data that is generally regarded as personal",
                    "* data has been removed from this object.",
                    "* To view the original object, please query the RIPE Database at:",
                    "* http://www.ripe.net/whois",
                    "****************************"
                ],
                "source": "RIPE"
            }
        ]
    }
}'''

_json_response_error = '''{
    "code": 403,
    "messages": "Access restricted. Check credits balance or enter the correct API key."
}'''


class TestModel(unittest.TestCase):

    def test_response_parsing(self):
        response = loads(_json_response_ok)
        parsed = Response(response)
        self.assertEqual(parsed.count, response['result']['count'])
        self.assertEqual(parsed.search, response['search'])
        self.assertIsInstance(parsed.inetnums, list)
        self.assertIsInstance(parsed.inetnums[0].description, list)
        self.assertListEqual(parsed.inetnums[0].description,
                             response['result']['inetnums'][0]['description'])
        self.assertIsInstance(parsed.inetnums[0].admin_contact, list)
        self.assertListEqual(parsed.inetnums[0].admin_contact[0].address,
                             response['result']['inetnums'][0]['adminContact'][0]['address'])
        self.assertDictEqual(vars(parsed.inetnums[0].AS),
                             response['result']['inetnums'][0]['as'])
        self.assertDictEqual(vars(parsed.inetnums[1].mnt_by[0]),
                             response['result']['inetnums'][1]['mntBy'][0])
        self.assertEqual(parsed.inetnums[0].org.name,
                         response['result']['inetnums'][0]['org']['name'])

    def test_error_parsing(self):
        error = loads(_json_response_error)
        parsed_error = ErrorMessage(error)
        self.assertEqual(parsed_error.code, error['code'])
        self.assertEqual(parsed_error.message, error['messages'])

    def test_comparing_two_models(self):
        model1 = Response(json.loads(_json_response_ok))
        model2 = Response(json.loads(_json_response_ok))
        self.assertEqual(model1, model2)
