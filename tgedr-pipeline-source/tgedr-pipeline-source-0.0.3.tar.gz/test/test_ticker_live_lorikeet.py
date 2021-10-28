import os

import pytest
from tgedr.pipeline.common.common import PipelineConfigException
from tgedr.pipeline.common.factory import Factory

RESOURCES_DIR = f"{os.path.dirname(os.path.realpath(__file__))}/resources"


def test_factory_get_source(monkeypatch):

    monkeypatch.setenv("CONFIGLOOKUP_DIR", RESOURCES_DIR)
    monkeypatch.setenv("CONFIGLOOKUP_FILE_PREFIX", "config")

    config = {
        "class": "TickerLiveLorikeet",
        "module": "tgedr.pipeline.source.ticker_live_lorikeet",
        "config": {"tickers": {"key": "ticker_live_lorikeet.tickers"}},
    }
    o = Factory.get_source(config=config)
    assert type(o).__name__ == "TickerLiveLorikeet", "oops wrong type"


def test_factory_get_source_2(monkeypatch):

    monkeypatch.setenv("CONFIGLOOKUP_DIR", RESOURCES_DIR)
    monkeypatch.setenv("CONFIGLOOKUP_FILE_PREFIX", "config")

    config = {
        "class": "TickerLiveLorikeet",
        "module": "tgedr.pipeline.source.ticker_live_lorikeet",
        "config": {"tickers": {"value": ["goog", "aapl"]}},
    }
    o = Factory.get_source(config=config)
    assert type(o).__name__ == "TickerLiveLorikeet", "oops wrong type"


def test_factory_get_not_valid_source():
    with pytest.raises(PipelineConfigException):
        config = {
            "class": "TickerLiveLorikeet",
            "module": "tgedr.pipeline.source.ticker_live_lorikeet",
            "config": {"dummy": 7},
        }
        Factory.get_source(config=config)


def test_sneak_peak(monkeypatch):
    monkeypatch.setenv("CONFIGLOOKUP_DIR", RESOURCES_DIR)
    monkeypatch.setenv("CONFIGLOOKUP_FILE_PREFIX", "config")

    config = {
        "class": "TickerLiveLorikeet",
        "module": "tgedr.pipeline.source.ticker_live_lorikeet",
        "config": {"tickers": {"value": ["goog", "aapl"]}},
    }
    o = Factory.get_source(config=config)
    assert 2 == len(o.get()), "oopps"
