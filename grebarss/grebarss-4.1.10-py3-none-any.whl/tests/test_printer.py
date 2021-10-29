"""This module contains tests for module printer.py."""

import os
import sys
from contextlib import redirect_stdout
from pathlib import Path

import pytest

sys.path.append(os.path.dirname(os.getcwd()))
sys.path.append(os.getcwd())

from grebarss_reader.printer import Printer


@pytest.fixture
def printer_instance():
    """
    Initialization object class Printer
    :return: object class Printer
    """
    return Printer()


@pytest.fixture
def sample_feed():
    """
    Create object sample_feed
    :return: object sample_feed
    """
    return {'item': [{'title': '«Для тестирования ёЙ', 'pubDate': "!@$%^*()/+- &#39", 'link': 'For test Q'}]}


def test_encoding_print_stdout(printer_instance, sample_feed, tmpdir):
    expected_data = '\n - - - - - - - - - - - - - - - - - - - -  \n\nTitle: «Для тестирования ёЙ\nData: !@$%^*()/+- &#39\nLink: For test Q\nImage: None\n'

    with open(Path(str(tmpdir), 'stdout.txt'), 'w', encoding='utf-8') as file:
        with redirect_stdout(file):
            printer_instance.print_info(sample_feed)

    with open(Path(str(tmpdir), 'stdout.txt'), 'r', encoding='utf-8') as file:
        printed_data = file.read()

    assert (printed_data == expected_data)


def test_encoding_print_json_stdout(printer_instance, sample_feed, tmpdir):
    expected_data = '\n - - - - - - - - - - - - - - - - - - - -  \n\n{"title": "«Для тестирования ёЙ", "pubDate": "!@$%^*()/+- &#39", "link": "For test Q"}\n'

    with open(Path(str(tmpdir), 'stdout.txt'), 'w', encoding='utf-8') as file:
        with redirect_stdout(file):
            printer_instance.print_info_json(sample_feed)

    with open(Path(str(tmpdir), 'stdout.txt'), 'r', encoding='utf-8') as file:
        printed_data = file.read()

    assert (printed_data == expected_data)
