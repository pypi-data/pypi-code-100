"""This module contains tests for module grebarss_parser.py"""

import os
import sys

import pytest

sys.path.append(os.path.dirname(os.getcwd()))
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), "grebarss_reader"))
print(sys.path)

from grebarss_reader.grebarss_parser import RssParser


@pytest.fixture
def sample_raw_feed():
    """
    Create object sample_raw_feed
    :return: object sample_raw_feed
    """
    raw_feed = {
        "rss": {
            "@version": "2.0",
            "@xmlns:content": "http://purl.org/rss/1.0/modules/content/",
            "channel": {
                "title": "Люди Onlíner",
                "link": "https://people.onliner.by/",
                "description": "Люди Onlíner",
                "pubDate": "Thu, 28 Oct 2021 20:10:13 +0300",
                "language": "ru",
                "image": {
                    "url": "https://content.onliner.by/pic/logo.png",
                    "width": "181",
                    "height": "53",
                    "title": "Люди Onlíner",
                    "link": "https://people.onliner.by/"
                },
                "item": [
                    {
                        "title": "Концерт Лободы перенесен",
                        "link": "https://people.onliner.by/2021/10/28/koncert-lobody-perenesen",
                        "pubDate": "Thu, 28 Oct 2021 20:10:13 +0300",
                        "dc:creator": "Onliner",
                        "category": "Культура",
                        "guid": {
                            "@isPermaLink": "false",
                            "#text": "https://people.onliner.by/2021/10/28/koncert-lobody-perenesen"
                        },
                        "description": "Светлана Лобода должна была дать шоу Boom-Boom!",
                        "media:thumbnail": {
                            "@url": "https://content.onliner.by/news/thumbnail/3d33bec0a75574948271cf565f6abc9c.jpeg"
                        }
                    }
                ]
            }
        }
    }
    return raw_feed


@pytest.fixture
def rss_parser_instance():
    """
    Initialization object class RssParser
    :return: object class RssParser
    """
    return RssParser()


@pytest.mark.parametrize('some_links, expected_links', [
    [{'url': 'https://image1.jpg'}, 'https://image1.jpg'],
    [{'url': [{'link': 'https://image2.jpeg'}]}, 'https://image2.jpeg'],
    [{'url': [{'https://image3.png': 'https://image4'}]}, 'https://image3.png'],
],
                         )
def test_get_image_link_get_valid_link(rss_parser_instance, some_links, expected_links):
    """
    Checks link format validation
    :param rss_parser_instance: object class RssParser
    :param some_links: sample some image link in feed
    :param expected_links: string with image link
    """
    got_links = rss_parser_instance._get_image_link(some_links)
    assert (got_links == expected_links)


def test_parse_xml_correct_parse(rss_parser_instance, sample_raw_feed):
    parsed_dict = rss_parser_instance._parse_xml(sample_raw_feed)
    expected_dict = {'item': [{'title': 'Концерт Лободы перенесен',
                               'pubDate': 'Thu, 28 Oct 2021 20:10:13 +0300',
                               'link': 'https://people.onliner.by/2021/10/28/koncert-lobody-perenesen',
                               'image': 'https://content.onliner.by/news/thumbnail/3d33bec0a75574948271cf565f6abc9c.jpeg'}]}
    assert (parsed_dict == expected_dict)


