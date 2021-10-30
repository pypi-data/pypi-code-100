"""This module contains tests for module converter.py."""

import os
import sys

import pytest

sys.path.append(os.path.dirname(os.getcwd()))
sys.path.append(os.getcwd())

from converter import Converter


@pytest.fixture
def converter_instance(tmpdir):
    """
    Initialization object class Converter
    :param tmpdir: object temp catalog
    :return: object class Converter
    """
    feed = {'item': [{'title': 'Концерт Лободы перенесен',
                               'pubDate': 'Thu, 28 Oct 2021 20:10:13 +0300',
                               'link': 'https://people.onliner.by/2021/10/28/koncert-lobody-perenesen',
                               'image': 'https://content.onliner.by/news/thumbnail/3d33bec0a75574948271cf565f6abc9c.jpeg'}]}
    return Converter('https://people.onliner.by/feed', feed, str(tmpdir))


def test_to_pdf_create_file(converter_instance):
    """
    Verifies that method to_pdf of class Converter creates a file
    :param converter_instance: object class Converter
    """
    converter_instance.to_pdf()
    assert (os.path.exists(os.path.join(converter_instance.folder_path, "news.pdf")) is True)


def test_to_html_create_file(converter_instance):
    """
    Verifies that method to_html of class Converter creates a file
    :param converter_instance: object class Converter
    """
    converter_instance.to_html()
    assert (os.path.exists(os.path.join(converter_instance.folder_path, "news.html")) is True)
