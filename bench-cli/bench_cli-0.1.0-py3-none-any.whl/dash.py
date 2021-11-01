import pandas as pd
import dash
import os
import base64
from inflection import humanize
from pathlib import Path
from sqlalchemy import create_engine, select, Table, MetaData
from sqlalchemy.orm import Session
from dash import dcc, html, Input, Output
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go


class Frame:
    def __init__(self):
        self.host = os.getenv("BENCH_DB_HOST")
        self.port = os.getenv("BENCH_DB_PORT")
        self.user = os.getenv("BENCH_DB_USER")
        self.dbname = os.getenv("BENCH_DB_NAME")
        self.password = os.getenv("BENCH_DB_PASSWORD")

    def engine(self):
        engine = create_engine(
            f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"
        )

        return engine

    def dataframe(self):
        connection = self.engine().connect()
        metadata = MetaData()
        metrics = Table("metrics", metadata, autoload_with=self.engine())
        stock = Table("stock", metadata, autoload_with=self.engine())
        query = select([stock, metrics]).join(
            stock, stock.columns.id == metrics.columns.stock_id
        )
        result = (connection.execute(query)).fetchall()
        raw_df = pd.DataFrame(result)
        raw_df.columns = result[0].keys()
        cols = [humanize(col) for col in list(raw_df.columns)]
        df = pd.DataFrame(result)
        df.columns = cols
        df.drop(
            ["Id", "Last updated", "Id 1", "Stock", "Period key"], axis=1, inplace=True
        )

        return df


class DashApp:
    def __init__(self, data, port=8050):
        self.data = data
        self.port = port

    def run(self, df):
        app = dash.Dash(external_stylesheets=[dbc.themes.ZEPHYR])
        app.title = "Bench"

        logo = str(Path("bench/assets/banner.png").resolve())
        encoded_image = base64.b64encode(open(logo, "rb").read())

        companies = list(df["Company"].unique())
        tickers = list(df["Symbol"].unique())

        company_list = dict(zip(companies, tickers))
        metrics_list = list(df.loc[:, "Gross margin":"Cash conversion cycle"].columns)
        year_list = sorted(list(df["Filing year"].unique()))
        quarter_list = sorted(list(df["Filing quarter"].unique()))

        stock_dropdown = [
            dbc.Row(
                [
                    dbc.Label("Symbol"),
                    dcc.Dropdown(
                        id="ticker-dropdown",
                        options=[
                            {"label": k, "value": company_list[k]} for k in company_list
                        ],
                        multi=True,
                    ),
                ],
                className="mb-3",
            ),
            dbc.Row(
                [
                    dbc.Label("Period"),
                    dcc.Dropdown(
                        id="period-dropdown",
                        options=[
                            {"label": "Annual", "value": "annual"},
                            {"label": "Quarterly", "value": "quarterly"},
                        ],
                    ),
                ],
                className="mb-3",
            ),
        ]

        benchmark = [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Row(
                                [
                                    dbc.Col([dbc.Label("Previous")]),
                                ]
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            dbc.Label("Year"),
                                            dcc.Dropdown(
                                                id="previous-year",
                                                options=[
                                                    {"label": val, "value": val}
                                                    for val in year_list
                                                ],
                                                placeholder="Year",
                                                style={
                                                    "font-size": "9px",
                                                    "width": "105%",
                                                },
                                            ),
                                        ],
                                        className="mb-3",
                                    ),
                                    dbc.Col(
                                        [
                                            dbc.Label("Quarter"),
                                            dcc.Dropdown(
                                                id="previous-quarter",
                                                options=[
                                                    {
                                                        "label": val,
                                                        "value": val,
                                                    }
                                                    for val in quarter_list
                                                ],
                                                placeholder="Q",
                                                style={
                                                    "font-size": "9px",
                                                    "width": "40%",
                                                },
                                            ),
                                        ],
                                        className="mb-3",
                                    ),
                                ]
                            ),
                        ]
                    ),
                    dbc.Col(
                        [
                            dbc.Row(
                                [
                                    dbc.Col([dbc.Label("Current")]),
                                ]
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            dbc.Label("Year"),
                                            dcc.Dropdown(
                                                id="current-year",
                                                options=[
                                                    {"label": val, "value": val}
                                                    for val in year_list
                                                ],
                                                placeholder="Year",
                                                style={
                                                    "font-size": "9px",
                                                    "width": "105%",
                                                },
                                            ),
                                        ],
                                        className="mb-3",
                                    ),
                                    dbc.Col(
                                        [
                                            dbc.Label("Quarter"),
                                            dcc.Dropdown(
                                                id="current-quarter",
                                                options=[
                                                    {
                                                        "label": val,
                                                        "value": val,
                                                    }
                                                    for val in quarter_list
                                                ],
                                                placeholder="Q",
                                                style={
                                                    "font-size": "9px",
                                                    "width": "40%",
                                                },
                                            ),
                                        ],
                                        className="mb-3",
                                    ),
                                ]
                            ),
                        ]
                    ),
                ]
            )
        ]

        metrics_dropdown = [
            dbc.Row(
                [
                    dcc.Dropdown(
                        id="metrics-dropdown",
                        options=[{"label": val, "value": val} for val in metrics_list],
                    ),
                ],
                className="mb-3",
            ),
        ]

        app.layout = dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Img(
                                            src="data:image/png;base64,{}".format(
                                                encoded_image.decode()
                                            ),
                                            style={
                                                "width": "30%",
                                                "float": "left",
                                            },
                                        )
                                    ],
                                    width=True,
                                )
                            ],
                            align="end",
                        ),
                        html.Hr(),
                        dbc.Col(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            width=100,
                                            children=dbc.Card(
                                                [
                                                    dbc.CardHeader("Parameters"),
                                                    dbc.CardBody(stock_dropdown),
                                                ],
                                                style={
                                                    "class": "card border-light mb-3"
                                                },
                                            ),
                                        )
                                    ],
                                    className="mb-3",
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            width=100,
                                            children=dbc.Card(
                                                [
                                                    dbc.CardHeader("Benchmark"),
                                                    dbc.CardBody(benchmark),
                                                ],
                                                style={
                                                    "class": "card border-light mb-3"
                                                },
                                            ),
                                        )
                                    ],
                                    className="mb-3",
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            width=100,
                                            children=dbc.Card(
                                                [
                                                    dbc.CardHeader("Metrics"),
                                                    dbc.CardBody(metrics_dropdown),
                                                ],
                                                style={
                                                    "class": "card border-light mb-3"
                                                },
                                            ),
                                        )
                                    ],
                                    className="mb-3",
                                ),
                            ],
                            className="col-4",
                        ),
                        dbc.Col(
                            [
                                dbc.Row(
                                    [
                                        html.Div(
                                            id="graph-container",
                                            children=[
                                                dcc.Graph(
                                                    id="bench-scatterplot",
                                                    style={
                                                        "position": "center",
                                                        "width": "100%",
                                                        "height": "100%",
                                                    },
                                                    config={"displayLogo": "False"},
                                                    responsive=True,
                                                )
                                            ],
                                            style={
                                                "class": "mb-3",
                                                "height": "80%",
                                                "position": "center",
                                            },
                                        ),
                                        html.Div(
                                            id="alert-container",
                                            children=[
                                                dbc.Alert(
                                                    "Select values to display the chart.",
                                                    color="warning",
                                                    style={
                                                        "color": "#856404",
                                                        "background-color": "#fff3cd",
                                                        "border-color": "#ffeeba",
                                                    },
                                                )
                                            ],
                                        ),
                                    ],
                                    style={"class": "mb-3", "height": "100%"},
                                )
                            ],
                            className="col-8",
                        ),
                    ],
                )
            ],
            fluid=True,
        )

        @app.callback(
            Output("previous-quarter", "disabled"),
            Output("current-quarter", "disabled"),
            Input("period-dropdown", "value"),
        )
        def disable_quarterly(value):
            if value == "annual":
                return [True, True]
            return [False, False]

        @app.callback(
            Output("graph-container", "style"),
            Output("alert-container", "style"),
            Input("ticker-dropdown", "value"),
            Input("period-dropdown", "value"),
            Input("previous-year", "value"),
            Input("previous-quarter", "value"),
            Input("current-year", "value"),
            Input("current-quarter", "value"),
            Input("metrics-dropdown", "value"),
        )
        def hide_containers(
            ticker_input,
            period_input,
            previous_year_input,
            previous_quarter_input,
            current_year_input,
            current_quarter_input,
            metrics_input,
        ):
            if period_input == "annual":
                if all(
                    [
                        ticker_input,
                        any([previous_year_input, current_year_input]),
                        metrics_input,
                    ]
                ):
                    return {"display": "block"}, {"display": "none"}
                else:
                    return {"display": "none"}, {"display": "block"}
            elif period_input == "quarterly":
                if all(
                    [
                        ticker_input,
                        previous_year_input,
                        previous_quarter_input,
                        current_year_input,
                        current_quarter_input,
                        metrics_input,
                    ]
                ):
                    return {"display": "block"}, {"display": "none"}
                else:
                    return {"display": "none"}, {"display": "block"}
            else:
                return {"display": "none"}, {"display": "block"}

        @app.callback(
            Output("bench-scatterplot", "figure"),
            Input("ticker-dropdown", "value"),
            Input("period-dropdown", "value"),
            Input("previous-year", "value"),
            Input("previous-quarter", "value"),
            Input("current-year", "value"),
            Input("current-quarter", "value"),
            Input("metrics-dropdown", "value"),
        )
        def update_figure(
            tickers,
            period,
            previous_year,
            previous_quarter,
            current_year,
            current_quarter,
            metric,
        ):
            if not all([tickers, metric, period]):
                raise PreventUpdate
            else:
                dff = df[df["Symbol"].isin(tickers)]
                if period == "quarterly":
                    dfff_curr = dff[
                        (dff["Period type"] == period)
                        & (dff["Filing year"] == current_year)
                        & (dff["Filing quarter"] == current_quarter)
                    ]
                    dfff_prev = dff[
                        (dff["Period type"] == period)
                        & (dff["Filing year"] == previous_year)
                        & (dff["Filing quarter"] == previous_quarter)
                    ]
                else:
                    dfff_curr = dff[
                        (dff["Period type"] == period)
                        & (dff["Filing year"] == current_year)
                    ]
                    dfff_prev = dff[
                        (dff["Period type"] == period)
                        & (dff["Filing year"] == previous_year)
                    ]

                metric_filter = f"{metric}"

                colors = [
                    "#323A59",
                    "#4F5B8C",
                    "#778DAA",
                    "#9C7975",
                    "#33121B",
                    "#690B14",
                    "#DA3626",
                    "#E65F25",
                    "#F38D20",
                    "#FDB913",
                ]

                fig = px.scatter(
                    dfff_curr,
                    y=metric_filter,
                    color="Symbol",
                    color_discrete_sequence=colors,
                    hover_data=[
                        "Symbol",
                        "Filing year",
                    ],
                ).update_traces(
                    legendgroup="symbol",
                    legendgrouptitle_text="",
                    hovertemplate="%{customdata[0]}<br>Year: %{customdata[1]}<br>%{y:.1f}",
                )

                fig2 = go.Figure(
                    fig.add_traces(
                        (
                            px.scatter(
                                dfff_prev,
                                y=metric_filter,
                                color="Symbol",
                                color_discrete_sequence=colors,
                                hover_data=[
                                    "Symbol",
                                    "Filing year",
                                ],
                            ).update_traces(
                                marker={"symbol": "circle-open"},
                                hovertemplate="%{customdata[0]}<br>Year: %{customdata[1]}<br>%{y:.1f}",
                            )
                        )._data
                    )
                )

                fig.update_layout(
                    {
                        "plot_bgcolor": "rgba(0,0,0,0)",
                        "paper_bgcolor": "rgba(0,0,0,0)",
                        "xaxis": dict(visible=False),
                    }
                )

                fig.update_traces(marker={"size": 12})
                fig.update_xaxes(
                    showspikes=True,
                    spikethickness=1,
                    spikesnap="cursor",
                    spikemode="across",
                )
                fig.update_yaxes(
                    showspikes=True,
                    spikethickness=1,
                    spikemode="across",
                    spikesnap="cursor",
                )

                return fig

        app.run_server(port=self.port)
