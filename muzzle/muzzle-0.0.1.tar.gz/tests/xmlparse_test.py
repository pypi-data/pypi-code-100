from muzzle_test import MuzzleTestCase
from muzzle import XMLParser
from xml.etree.ElementTree import Element


class TestXmlParse(MuzzleTestCase):
    def test_parse_xml(self, odata_xml):
        parser = XMLParser()
        obj = parser.parse(odata_xml)
        assert isinstance(obj, Element), "{obj} is not an XML object"
