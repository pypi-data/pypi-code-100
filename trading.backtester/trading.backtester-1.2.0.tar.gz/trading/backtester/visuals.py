"""Module containing visualizations."""
# pylint: disable=line-too-long

from __future__ import annotations

import math

from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import quantstats as qs

from trading.backtester import position as position_lib


def visualize(
    self,
    input_symbol: str | None = None,
    plots: list | dict | str | None = None,
) -> go.Figure | None:
    """Visualization function for the backtester.

    Arguments:
        input_symbol: The asset symbol that we want to visualize. If
            set to `None`, then the results of the visualization is for
            the overall backtest result.
        plots: A list of strings indicating the indicators, and other
            charts that we want to include in the visualization.
    """

    if plots and not isinstance(plots, (dict, list, tuple, str)):
        return None

    # Turn plots into configs
    if plots is None:
        if input_symbol is None:
            plots = ["equity", "drawdown"]
        else:
            plots = []
            show_candlesticks = True

    show_trades = False if not plots else "trades" in plots
    show_candlesticks = False if not plots else ("candles" in plots or "ohlcv" in plots)
    show_positions = False if not plots else "position_size" in plots

#     if not show_candlesticks and show_trades and input_symbol:
#         show_candlesticks = True

    if isinstance(plots, dict):
        plot_configs = plots
    elif isinstance(plots, str):
        plot_configs = {str(plots): {}}
    else:
        plot_configs = {plot_name: {} for plot_name in plots}

    # Make sure the symbol is given for graphs other than equity and dd
    for plot_name in plot_configs.keys():
        if (plot_name not in ("equity", "drawdown") and
            input_symbol is None
        ):
            return None


    DEFAULT_CONFIG = {
        "color": "rgba(66,133,244,1)",
        "width": 2,
    }

    # Auto fetch trading and signal source symbols
    trading_symbol = None
    signal_source_symbol = None
    if input_symbol:
        for asset in self.config.assets:
            if (input_symbol == asset.trading_symbol or
                input_symbol == asset.signal_source_symbol
           ):
                trading_symbol = asset.trading_symbol
                signal_source_symbol = asset.signal_source_symbol

        if trading_symbol is None and signal_source_symbol is None:
            return None

    first_signal_source_symbol = list(self.exchange.data.keys())[0]
    universal_x = self.exchange.data[first_signal_source_symbol].index

    # fig = go.Figure()
    if show_candlesticks and "equity" in plots and "drawdown" in plots:
        fig = make_subplots(rows=3, cols=1)
        drawdown_row, equity_row, ohlcv_row = (1, 2, 3)
    elif not show_candlesticks and "equity" in plots and "drawdown" in plots:
        if len(plots) >= 3:
            fig = make_subplots(rows=3, cols=1)
            drawdown_row, equity_row, ohlcv_row = (1, 2, 3)
        else:
            fig = make_subplots(rows=2, cols=1)
            drawdown_row, equity_row, ohlcv_row = (1, 2, None)
    elif len(plots) >= 2:
        if (("equity" in plots and "drawdown" not in plots) or
            ("drawdown" in plots and "equity" not in plots)
       ):
            fig = make_subplots(rows=2, cols=1)
            drawdown_row, equity_row, ohlcv_row = (1, 1, 2)
        else:
            fig = make_subplots(rows=1, cols=1)
            drawdown_row, equity_row, ohlcv_row = (1, 1, 1)
    else:
        fig = make_subplots(rows=1, cols=1)
        drawdown_row, equity_row, ohlcv_row = (1, 1, 1)

    if show_candlesticks and input_symbol is not None:
        ohlcv = go.Candlestick(
            x=self.exchange.data[signal_source_symbol].index,
            open=self.exchange.data[signal_source_symbol].open,
            high=self.exchange.data[signal_source_symbol].high,
            low=self.exchange.data[signal_source_symbol].low,
            close=self.exchange.data[signal_source_symbol].close,
            name="OHLCV")

        fig.add_trace(ohlcv, row=ohlcv_row, col=1)

        cs = fig.data[0]

        # Set line and fill colors for OHLCV
        cs.increasing.fillcolor = "rgba(38,166,154,0.6)"
        cs.increasing.line.color = "rgba(38,166,154,1)"
        cs.decreasing.fillcolor = "rgba(239,83,80,0.6)"
        cs.decreasing.line.color = "rgba(239,83,80,1)"

    if "candles" in plot_configs:
        del plot_configs["candles"]

    if "equity" in plot_configs:
        plot_config = DEFAULT_CONFIG.copy()
        plot_config.update({"color": "#222222"})
        if input_symbol is not None:
            equity_x = self.exchange.asset[trading_symbol].financials.index
            equity_y = self.exchange.asset[trading_symbol].financials.equity
            # equity_y = [(e / self.exchange.initial_balance) - 1 for e in equity_y]
            equity = go.Scatter(
                line=plot_config,
                x=equity_x,
                y=equity_y,
                mode="lines",
                fill="tozeroy",
                fillcolor="rgba(0,0,0,0.1)",
                name="Equity")

        else:
            equity_x = self.exchange.financials.index
            equity_y = self.exchange.financials.equity
            equity = go.Scatter(
                line=plot_config,
                x=equity_x,
                y=equity_y,
                # y=equity_y / self.exchange.initial_balance) - 1,
                mode="lines",
                fill="tozeroy",
                fillcolor="rgba(0,0,0,0.1)",
                name="Equity")

        fig.add_trace(equity, row=equity_row, col=1)
        fig.update_layout(**{
            f"yaxis{equity_row}": dict(range=[
                min(equity_y), max(equity_y)
            ])
        })
        del plot_configs["equity"]

    if "drawdown" in plot_configs:
        if input_symbol is None:
            equity_series = pd.Series(self.exchange.financials.equity)
        else:
            equity_series = pd.Series(self.exchange.asset[trading_symbol].financials.equity)

        first_symbol = list(self.exchange.asset.keys())[0]
        drawdown = qs.stats.to_drawdown_series(equity_series) * 100
        plot_config = DEFAULT_CONFIG.copy()
        plot_config.update({"color": "rgba(239,67,55,1)"})
        equity = go.Scatter(
            line=plot_config,
            x=universal_x,
            y=drawdown,
            mode="lines",
            fill="tozeroy",
            fillcolor="rgba(239,67,55,0.1)",
            name="Drawdown")

        fig.add_trace(equity, row=drawdown_row, col=1)
        del plot_configs["drawdown"]

    if show_trades:
        del plot_configs["trades"]

        closed_timestamps = [t.closing_timestamp for t in self.exchange.asset[trading_symbol].closed_trades]

        for trade in self.exchange.asset[trading_symbol].closed_trades + self.exchange.asset[trading_symbol].open_trades:
            if trade.trading_symbol != trading_symbol:
                continue

            if trade.closing_timestamp and trade.close:
                if trade.execution_timestamp in closed_timestamps:
                    actual_trade_ay = 96
                    actual_trade_standoff = 58
                else:
                    actual_trade_ay = 38
                    actual_trade_standoff = 0

                fig.add_annotation(
                    x=trade.closing_timestamp,  # arrows' head
                    y=trade.close,
                    ax=trade.closing_timestamp,  # arrows' tail
                    ay=-38 if trade.position == position_lib.LONG else 38,
                    xref=f"x{ohlcv_row}",
                    yref=f"y{ohlcv_row}",
                    axref=f"x{ohlcv_row}",
                    ayref="pixel",
                    text=(
                        f"Close {trade.id}<br>{(trade.position_multiplier * -trade.qty):+.4f}"
                        if trade.position == position_lib.SHORT
                        else f"{(trade.position_multiplier * -trade.qty):+.4f}<br>Close {trade.id}"
                    ),
                    font=dict(
                        family="Trebuchet MS, Roboto, Ubuntu, sans-serif",
                        size=12,
                    ),
                    # text=f"{trade.position_word}<br>{(trade.position_multiplier * trade.qty)}",  # if you want only the arrow
                    showarrow=True,
                    arrowhead=2,
                    arrowsize=1,
                    arrowwidth=2,
                    arrowcolor='#d500f9',
                )

            else:
                actual_trade_ay = 38
                actual_trade_standoff = 0

            if (trade.closing_timestamp is None and
                trade.execution_timestamp and
                trade.execution_timestamp in closed_timestamps
            ):
                actual_trade_ay = 96
                actual_trade_standoff = 58

            fig.add_annotation(
                x=trade.execution_timestamp,  # arrows' head
                y=trade.limit,
                ax=trade.execution_timestamp,  # arrows' tail
                ay=actual_trade_ay * trade.position_multiplier,
                xref=f"x{ohlcv_row}",
                yref=f"y{ohlcv_row}",
                axref=f"x{ohlcv_row}",
                text=(
                    f"{(trade.position_multiplier * trade.qty):+.4f}<br>{trade.id}"
                    if trade.position == position_lib.SHORT
                    else f"{trade.id}<br>{(trade.position_multiplier * trade.qty):+.4f}"
                ),
                font=dict(
                    family="Segoe UI, Roboto, Ubuntu, sans-serif",
                    size=12,
                ),
                # text=f"{trade.position_word}<br>{(trade.position_multiplier * trade.qty)}",  # if you want only the arrow
                showarrow=True,
                standoff=actual_trade_standoff,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor='rgba(66,133,244,1)' if trade.position == position_lib.LONG else 'rgba(239,67,55,1)'
            )

    COLORS = ["#2962ff", "#673ab7", "#9c27b0", "#e91e63", "#f44336", "#ff9800", "#4caf50", "#009688", "#00bcd4"]
    for i, (plot_name, plot_config_override) in enumerate(plot_configs.items()):
        plot_config = {
            "color": COLORS[i % (len(COLORS) + 1)],
            "width": 2,
        }
        plot_config.update(plot_config_override)

        plot_obj = go.Scatter(
            line=plot_config,
            x=self.exchange.data[signal_source_symbol].index,
            y=self.exchange.data[signal_source_symbol][plot_name],
            name=plot_name.title())

        fig.add_trace(plot_obj, row=ohlcv_row, col=1)

    fig.update_layout(
        margin=dict(l=15, r=15, t=40, b=15),
        plot_bgcolor="rgba(255,255,255,1)",
        paper_bgcolor="rgba(255,255,255,0)",
    )

    fig.update_xaxes(showgrid=False, rangeslider_visible=False)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#dadce0")
    fig.update_xaxes(zeroline=True, zerolinewidth=2, zerolinecolor="#dadce0")
    fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor="#dadce0")

    # fig.update_layout(legend_title_text='Subplots')
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0
    ))

    return fig
