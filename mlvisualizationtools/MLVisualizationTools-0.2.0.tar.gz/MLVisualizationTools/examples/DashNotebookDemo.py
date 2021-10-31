from MLVisualizationTools import Analytics, Interfaces, Graphs, Colorizers
from MLVisualizationTools.backend import fileloader
import pandas as pd
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' #stops agressive error message printing
from tensorflow import keras

try:
    from jupyter_dash import JupyterDash

    from dash import Input, Output
    from dash import dcc
    from dash import html
    import dash_bootstrap_components as dbc
    import plotly
except:
    raise ImportError("Dash and plotly are required to run this demo. Install them with the [dash] flag"
                      " on installation of this library.")

class App:
    def __init__(self):
        self.app = JupyterDash(__name__, title="Example Dash App")

        self.model = keras.models.load_model(fileloader('examples/Models/titanicmodel'))
        self.df: pd.DataFrame = pd.read_csv(fileloader('examples/Datasets/Titanic/train.csv'))

        options = []
        for col in self.df.columns:
            if col != "Survived":
                options.append({'label': col, 'value': col})

        self.AR = Analytics.Tensorflow(self.model, self.df, ["Survived"])
        self.maxvar = self.AR.maxVariance()

        self.x = self.maxvar[0].name
        self.y = self.maxvar[1].name

        self.fig = self.updateGraph()

        graph = dbc.Card([
            dcc.Graph(id='example-graph', figure=self.fig)
        ], body=True)

        config = dbc.Card([
            dbc.Label("X Axis: "),
            dcc.Dropdown(id='xaxis', options=options, value=self.x),
            html.Br(),
            dbc.Label("Y Axis: "),
            dcc.Dropdown(id='yaxis', options=options, value=self.y),
            html.Br(),
        ], body=True)

        self.app.layout = dbc.Container([
            html.H1("Dash Interactive ML Demo"),
            html.Hr(),
            dbc.Row([
                dbc.Col(config, md=4),
                dbc.Col(graph, md=8)]
            ),
            html.P()])

        inputs = [Input('xaxis', "value"), Input('yaxis', 'value')]
        self.app.callback(Output("example-graph", "figure"), inputs)(self.updateGraphFromWebsite)

    def run(self):
        self.app.run_server(mode='external',host="0.0.0.0", port=1005)

    def updateGraph(self):
        data = Interfaces.TensorflowGrid(self.model, self.x, self.y, self.df, ["Survived"])
        data = Colorizers.Binary(data, highcontrast=True)
        self.fig = Graphs.PlotlyGrid(data, self.x, self.y)
        return self.fig

    def updateGraphFromWebsite(self, x, y):
        self.x = x
        self.y = y
        return self.updateGraph()

App().run()