"""Tests for trading.backtester.config."""

import copy

import pytest

import trading.backtester as bt


class TestBacktesterConfig:

    def test_backtester_config_class_is_visible(self):
        assert hasattr(bt, "BacktesterConfig")

    def test_from_dict_no_errors(self, input_dict_config):
        config = bt.BacktesterConfig.from_dict(input_dict_config)
        assert isinstance(config, bt.BacktesterConfig)

    def test_from_json_no_errors(self, input_json_config):
        config = bt.BacktesterConfig.from_json(input_json_config)
        assert isinstance(config, bt.BacktesterConfig)

    def test_from_json_invalid_json_error(self):
        with pytest.raises(ValueError):
            bt.BacktesterConfig.from_json("Non-JSON input")

    def test_load_no_errors(self, input_dict_config, input_json_config):
        config_from_dict = bt.BacktesterConfig.load(input_dict_config)
        assert isinstance(config_from_dict, bt.BacktesterConfig)
        assert config_from_dict.raw == input_dict_config

        config_from_json = bt.BacktesterConfig.load(input_json_config)
        assert isinstance(config_from_json, bt.BacktesterConfig)
        assert config_from_json.raw == input_dict_config
        assert config_from_json == config_from_dict

        # Use previously parsed configuration
        config_from_config = bt.BacktesterConfig.load(config_from_json)
        assert isinstance(config_from_config, bt.BacktesterConfig)
        assert config_from_config.raw == input_dict_config
        assert config_from_config == config_from_dict
        assert config_from_config == config_from_json
        assert config_from_json == config_from_dict

    def test_load_invalid_input_json_config_error(self):
        with pytest.raises(ValueError):
            bt.BacktesterConfig.load("Non-JSON input")

    def test_load_invalid_input_dict_config_error(self):
        with pytest.raises(ValueError):
            bt.BacktesterConfig.load(None)

        with pytest.raises(TypeError):
            bt.BacktesterConfig.load([1, 2, 3])

        with pytest.raises(ValueError):
            bt.BacktesterConfig.load({"unknown_key": []})

        with pytest.raises(TypeError):
            bt.BacktesterConfig.load({"assets": 1, "strategy_parameters": 1})

        with pytest.raises(TypeError):
            bt.BacktesterConfig.load({"assets": [1], "strategy_parameters": 1})

        with pytest.raises(TypeError):
            bt.BacktesterConfig.load(
                {"assets": [1], "strategy_parameters": {}})

    def test_load_set_start_older_than_end(self, input_dict_config):
        modified_config = copy.deepcopy(input_dict_config)
        modified_config["starting_timestamp"] = "2021-01-01 00:00:00"
        modified_config["ending_timestamp"] = "2020-01-01 00:00:00"

        with pytest.raises(ValueError):
            bt.BacktesterConfig.load(modified_config)

    def test_load_percent_total_allocation_to_53(self, input_dict_config):
        modified_config = copy.deepcopy(input_dict_config)
        modified_config["assets"][0]["allocation"] = 0

        with pytest.raises(ValueError):
            bt.BacktesterConfig.load(modified_config)

    def test_load_set_currency_to_unknown_value(self, input_dict_config):
        modified_config = copy.deepcopy(input_dict_config)
        modified_config["initial_balance_currency"] = "UNKNOWN"

        with pytest.raises(ValueError):
            bt.BacktesterConfig.load(modified_config)

    def test_backtester_config_strategy_parameters(self, input_json_config):
        config = bt.BacktesterConfig.from_json(input_json_config)

        assert config.strategy_parameters.length == 34
        assert config.strategy_parameters.multiplier == 1.5

    def test_backtester_config_root_level_properties(self, input_dict_config):
        config = bt.BacktesterConfig.from_dict(input_dict_config)

        assert config.initial_balance == 53.0091
        assert config.initial_balance_currency == "BTC"
        assert config.shared_balance == True
        assert config.trading_exchange == "bitmex"
        assert config.starting_timestamp == "2020-01-01 00:00:00"
        assert config.ending_timestamp == "2021-01-01 00:00:00"

    def test_backtester_config_asset_1(self, input_dict_config):
        config = bt.BacktesterConfig.from_dict(input_dict_config)

        assert config.assets[0].trading_symbol == "ADAUSD"
        assert config.assets[0].trading_timeframe == "4h"
        assert config.assets[0].signal_source_exchange == "binance"
        assert config.assets[0].signal_source_symbol == "ADA/USDT"
        assert config.assets[0].signal_timeframe == "4h"
        assert config.assets[0].allocation == 0.47

    def test_backtester_config_asset_2(self, input_dict_config):
        config = bt.BacktesterConfig.from_dict(input_dict_config)

        assert config.assets[1].trading_symbol == "XBTUSD"
        assert config.assets[1].trading_timeframe == "4h"
        assert config.assets[1].signal_source_exchange == "binance"
        assert config.assets[1].signal_source_symbol == "BTC/USDT"
        assert config.assets[1].signal_timeframe == "4h"
        assert config.assets[1].allocation == 0.53
