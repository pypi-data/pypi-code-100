import requests

import os
import sys

import pytest

sys.path.append(os.path.dirname(os.getcwd()))
sys.path.append(os.getcwd())

from grebarss_reader.getter import GetterXml


@pytest.fixture
def sample_500_response():
    """
    Create object response 500
    :return: object response 500
    """
    response = requests.get("https://google.com")
    response.status_code = 500
    return response


@pytest.fixture
def getterxml_instance():
    """
        Initialization object class GetterXml
        :return: object class GetterXml
        """
    return GetterXml()


def test_is_response_status_200(getterxml_instance, sample_500_response):
    assert (getterxml_instance._is_response_status_200(sample_500_response) == False)


def test_get_response(getterxml_instance):
    response = getterxml_instance.get_response("https://google.com")
    assert (response != None)
