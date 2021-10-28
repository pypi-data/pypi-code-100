import pytest

from tgedr.pipeline.common.common import PipelineConfigException
from tgedr.pipeline.common.factory import Factory


def test_factory_get_sink():
    config = {
        "class": "DummyPipelineSink",
        "module": "tgedr.pipeline.common.impl.dummy",
        "config": {"s": 2, "valid": True},
    }
    o = Factory.get_sink(config=config)
    assert type(o).__name__ == "DummyPipelineSink", "oops wrong type"


def test_factory_get_source():
    config = {
        "class": "DummyPipelineSource",
        "module": "tgedr.pipeline.common.impl.dummy",
        "config": {"s": 2, "valid": True},
    }
    o = Factory.get_source(config=config)
    assert type(o).__name__ == "DummyPipelineSource", "oops wrong type"


def test_factory_get_not_valid_source():
    with pytest.raises(PipelineConfigException):
        config = {
            "class": "DummyPipelineSource",
            "module": "tgedr.pipeline.common.impl.dummy",
            "config": {"s": 7, "valid": False},
        }
        Factory.get_source(config=config)


def test_factory_get_not_valid_sink():
    with pytest.raises(PipelineConfigException):
        config = {
            "class": "DummyPipelineSink",
            "module": "tgedr.pipeline.common.impl.dummy",
            "config": {"s": 2, "valid": False},
        }
        Factory.get_sink(config=config)
