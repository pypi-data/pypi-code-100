import json
import os

import pytest
from configlookup.main import Configuration
from tgedr.pipeline.common.common import PipelineConfigException
from tgedr.pipeline.common.factory import Factory

RESOURCES_DIR = f"{os.path.dirname(os.path.realpath(__file__))}/resources"


def test_azure_storage_queue_config_validation():
    with pytest.raises(PipelineConfigException):
        config = {
            "class": "AzureStorageQueue",
            "module": "tgedr.pipeline.sink.azure_storage_queue",
            "config": {"dummy": 7},
        }
        Factory.get_sink(config=config)


# just for manual test purposes while we don't mock a storage account
@pytest.mark.skip
def test_assert_azure_storage_queue(monkeypatch):

    monkeypatch.setenv("CONFIGLOOKUP_DIR", RESOURCES_DIR)
    sink = Factory.get_sink(config=Configuration.get("tgedr.pipeline.sink.test_azure_storage_queue"))
    assert sink is not None, "no sink here"
    assert not sink._assert_queue(), "it should not have the queue"


# just for manual test purposes while we don't mock a storage account
@pytest.mark.skip
def test_insert_in_azure_storage_queue(monkeypatch):
    monkeypatch.setenv("CONFIGLOOKUP_DIR", RESOURCES_DIR)
    sink = Factory.get_sink(config=Configuration.get("tgedr.pipeline.sink.test_azure_storage_queue"))
    message = json.dumps({"axe": "fdljasfaÊ"}, ensure_ascii=False)
    sink.put(msg=message)
    assert True, "oops, couldn't send message"
