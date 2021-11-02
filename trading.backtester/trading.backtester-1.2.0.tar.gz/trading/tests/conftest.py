"""Test fixtures for trading.backtester."""

import json as jsonlib

import pytest


@pytest.fixture(name="input_dict_config", scope="session")
def fixture_input_dict_config():
    return {
        "strategy_parameters": {
            "length": 34,
            "multiplier": 1.5
        },
        "initial_balance": 53.0091,
        "initial_balance_currency": "XBT",
        "shared_balance": True,
        "trading_exchange": "bitmex",
        "starting_timestamp": "2020-01-01 00:00:00",
        "ending_timestamp": "2021-01-01 00:00:00",
        "assets": [
            {
                "trading_symbol": "ADAUSD",
                "trading_timeframe": "4h",
                "signal_source_exchange": "binance",
                "signal_source_symbol": "ADA/USDT",
                "signal_timeframe": "4h",
                "allocation": 0.47,
            },
            {
                "trading_symbol": "XBTUSD",
                "trading_timeframe": "4h",
                "signal_source_exchange": "binance",
                "signal_source_symbol": "BTC/USDT",
                "signal_timeframe": "4h",
                "allocation": 0.53,
            }
        ]
    }


@pytest.fixture(name="input_json_config", scope="session")
def fixture_input_json_config(input_dict_config):
    return jsonlib.dumps(input_dict_config)


@pytest.fixture(name="golden_cross_input_config", scope="session")
def fixture_golden_cross_input_config():
    return {
        "strategy_parameters": {
            "fast_period": 50,
            "slow_period": 200
        },
        "initial_balance": 100000,
        "initial_balance_currency": "USD",
        "shared_balance": False,
        "trading_exchange": "bitmex",
        "starting_timestamp": "2018-03-04 00:00:00",
        "ending_timestamp": "2018-04-09 00:00:00",
        "assets": [
            {
                "trading_symbol": "XBTUSD",
                "trading_timeframe": "1d",
                "signal_source_exchange": "binance",
                "signal_source_symbol": "BTC/USDT",
                "signal_timeframe": "1d",
                "allocation": 1,
            }
        ]
    }


@pytest.fixture(name="no_parameters_input_config", scope="session")
def fixture_no_parameters_input_config():
    return {
        "strategy_parameters": {},
        "initial_balance": 1000,
        "initial_balance_currency": "USD",
        "shared_balance": False,
        "trading_exchange": "bitmex",
        "starting_timestamp": "2020-03-04 00:00:00",
        "ending_timestamp": "2020-04-09 00:00:00",
        "assets": [
            {
                "trading_symbol": "ETHUSD",
                "trading_timeframe": "4h",
                "signal_source_exchange": "binance",
                "signal_source_symbol": "ETH/USDT",
                "signal_timeframe": "4h",
                "allocation": 0.5,
            },
            {
                "trading_symbol": "BTCUSD",
                "trading_timeframe": "4h",
                "signal_source_exchange": "binance",
                "signal_source_symbol": "BTC/USDT",
                "signal_timeframe": "4h",
                "allocation": 0.2,
            },
            {
                "trading_symbol": "ADAUSD",
                "trading_timeframe": "4h",
                "signal_source_exchange": "binance",
                "signal_source_symbol": "ADA/USDT",
                "signal_timeframe": "4h",
                "allocation": 0.3,
            }
        ]
    }
