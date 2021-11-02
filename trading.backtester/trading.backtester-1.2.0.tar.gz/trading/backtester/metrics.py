"""Module containing metrics for the Backtester."""

import numpy as np
import pandas as pd
import quantstats as qs


class Metrics:
    def __init__(self, backtester):
        self._backtester = backtester

    def cagr(self, by_year: bool = True, rf: float = 0.0, compounded: bool = True):
        if not by_year:
            return qs.stats.cagr(self.returns, rf=rf, compounded=compounded)
        # for yearly_equity_df

    def calmar(self, prepare_returns: bool = True):
        return qs.stats.calmar(self.returns, prepare_returns=prepare_returns)

    def common_sense_ratio(self, prepare_returns: bool = True):
        return qs.stats.common_sense_ratio(
            self.returns, prepare_returns=prepare_returns)

    def cpc_index(self, prepare_returns: bool = True):
        return qs.stats.cpc_index(
            self.returns, prepare_returns=prepare_returns)

    def gain_to_pain_ratio(self, rf: float = 0, resolution: str = "D"):
        return qs.stats.gain_to_pain_ratio(
            self.returns, rf=rf, resolution=resolution)

    def kelly_criterion(self, prepare_returns: bool = True):
        return qs.stats.kelly_criterion(
            self.returns, prepare_returns=prepare_returns)

    def kurtosis(self, prepare_returns: bool = True):
        return qs.stats.kurtosis(self.returns, prepare_returns=prepare_returns)

    def max_drawdown(self):
        return qs.stats.max_drawdown(self.returns)

    def omega(self, rf: float = 0.0, required_return=0.0):
        return qs.stats.omega(
            self.returns, rf=rf, required_return=required_return, periods=365)

    def outlier_loss_ratio(
        self,
        quantile: float = 0.01,
        prepare_returns: bool = True,
    ):

        return qs.stats.outlier_loss_ratio(
            self.returns, quantile=quantile, prepare_returns=prepare_returns)

    def outlier_win_ratio(
        self,
        quantile: float = 0.99,
        prepare_returns: bool = True,
    ):

        return qs.stats.outlier_win_ratio(
            self.returns, quantile=quantile, prepare_returns=prepare_returns)

    def payoff_ratio(self, prepare_returns: bool = True):
        return qs.stats.payoff_ratio(
            self.returns, prepare_returns=prepare_returns)

    def profit_factor(self, prepare_returns: bool = True):
        return qs.stats.profit_factor(
            self.returns, prepare_returns=prepare_returns)

    def profit_ratio(self, prepare_returns: bool = True):
        return qs.stats.profit_ratio(
            self.returns, prepare_returns=prepare_returns)

    def rar(self, rf: float = 0.0):
        return qs.stats.rar(self.returns, rf=rf)

    def recovery_factor(self, prepare_returns: bool = True):
        return qs.stats.recovery_factor(
            self.returns, prepare_returns=prepare_returns)

    def risk_of_ruin(self, prepare_returns: bool = True):
        return qs.stats.risk_of_ruin(
            self.returns, prepare_returns=prepare_returns)

    def risk_return_ratio(self, prepare_returns: bool = True):
        return qs.stats.risk_return_ratio(
            self.returns, prepare_returns=prepare_returns)

    def ror(self):
        return qs.stats.ror(self.returns)

    def rolling_sortino(self):
        return qs.stats.rolling_sortino(
            self.returns, rolling_periods=182.5, periods=365, annualize=True)

    def serenity_index(self, rf: float = 0.0):
        return qs.stats.serenity_index(self.returns, rf=rf)

    def sharpe(self, by_year: bool = True): #### Goods
        indices = []
        sharpes = []

        if by_year:
            indices += list(self.returns(by_year=True).keys())
            sharpes += [qs.stats.sharpe(returns_df, periods=365, annualize=True) for returns_df in self.returns(by_year=True).values()]

        indices += [""]
        sharpes += [qs.stats.sharpe(self.returns(by_year=False), periods=365, annualize=True)]
        sharpe_df = pd.DataFrame({"Sharpe": sharpes}, index=indices)

        return sharpe_df

    def skew(self, prepare_returns: bool = True):
        return qs.stats.skew(self.returns, prepare_returns=prepare_returns)

    def sortino(self, by_year: bool = True): #### Goods
        indices = []
        sortinos = []

        if by_year:
            indices += list(self.returns(by_year=True).keys())
            sortinos += [float(qs.stats.sortino(returns_df, periods=365, annualize=True)) for returns_df in self.returns(by_year=True).values()]

        indices += [""]
        sortinos += [float(qs.stats.sortino(self.returns(by_year=False), periods=365, annualize=True))]
        sortino_df = pd.DataFrame({"Sortino": sortinos}, index=indices)

        return sortino_df

    def total_pnl(self, by_year: bool = False): #### Goods
        indices = []
        total_pnls = []

        if by_year:
            indices += list(self.returns(by_year=True).keys())
            total_pnls += [float(qs.stats.comp(returns_df) + 1) for returns_df in self.returns(by_year=True).values()]

        indices += [""]
        total_pnls += [float(qs.stats.comp(self.returns(by_year=False)) + 1)]
        total_pnl_df = pd.DataFrame({"Total PnL": total_pnls}, index=indices)

        return total_pnl_df

    def ulcer_index(self):
        return qs.stats.ulcer_index(self.returns)

    def ulcer_performance_index(self, rf: float = 0.0):
        return qs.stats.ulcer_performance_index(self.returns, rf=rf)

    def upi(self, rf: float = 0.0):
        return qs.stats.upi(self.returns, rf=rf)

    def value_at_risk(
        self,
        sigma: float = 1,
        confidence: float = 0.95,
        prepare_returns: bool = True,
    ):

        return qs.stats.value_at_risk(
            self.returns,
            sigma=sigma,
            confidence=confidence,
            prepare_returns=prepare_returns)

    def win_loss_ratio(self, prepare_returns: bool = True):
        return qs.stats.win_loss_ratio(
            self.returns, prepare_returns=prepare_returns)

    def equity(self, by_year: bool = True): #### Goods
        equity_df = self.bt.exchange.financials.equity

        if not by_year:
            return equity_df

        yearly_equity_df = {}
        for year in equity_df.index.year.unique():
            yearly_equity_df[int(year)] = equity_df[equity_df.index.year == year]

        return yearly_equity_df

    def returns(self, by_year: bool = True): #### Goods
        if not by_year:
            return self.equity(by_year=False).pct_change().fillna(0)

        return {
            year: equity_df.pct_change().fillna(0)
            for year, equity_df in self.equity(by_year=by_year).items()
        }

    @property
    def score(self):
        return (
            0.4 * self.sortino() +
            0.2 * (
                self.sharpe() +
                self.total_pnl() +
                self.average_return / self.max_drawdown()
            )
        )

    def average_return(self, by_year: bool = False): #### Goods
        indices = []
        average_returns = []

        if by_year:
            indices += list(self.returns(by_year=True).keys())
            average_returns += [returns_df.mean() for returns_df in self.returns(by_year=True).values()]

        indices += [""]
        average_returns += [float(self.returns(by_year=False).mean())]
        average_return_df = pd.DataFrame({"Average Return": average_returns}, index=indices)

        return average_return_df

    @property
    def bt(self): #### Goods
        return self._backtester

    @property
    def backtester(self): #### Goods
        return self._backtester

    @property
    def years(self): #### Goods
        return self.equity(by_year=False).index.year.unique()
