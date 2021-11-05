from MLVisualizationTools import Analytics, Interfaces, Graphs, Colorizers
from MLVisualizationTools.dashbackend import getTheme, getDashApp
from SingletonProcess import VBSingletonProcess
import pandas as pd

#TODO - tour

try:
    import dash
    from dash import Input, Output
    from dash import dcc
    from dash import html
    import dash_bootstrap_components as dbc
    import plotly
except ImportError:
    raise ImportError("Dash and plotly are required to use this tool. Install them with the [dash] flag"
                      " on installation of this library.")

class App:
    def __init__(self, model, data: pd.DataFrame, title:str = "DashModelVisualizer", theme:str = "dark", folder = None,
                 highcontrast:bool = True, notebook:bool = False, kagglenotebook:bool = False, mode:str = 'external',
                 host:str = '0.0.0.0', port: bool = None):

        theme, folder, self.figtemplate = getTheme(theme, folder)
        self.app, self.runFunc = getDashApp(title, notebook, kagglenotebook, host, port, mode, theme, folder)

        self.model = model
        self.df = data
        self.highcontrast = highcontrast

        options = []
        for col in self.df.columns:
            options.append({'label': col, 'value': col})

        self.AR = Analytics.Tensorflow(self.model, self.df)
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
            html.H1(title),
            html.Hr(),
            dbc.Row([
                dbc.Col(config, md=4),
                dbc.Col(graph, md=8)]
            ),
            html.P()],
            fluid=True,
            className='dash-bootstrap'
        )

        inputs = [Input('xaxis', "value"), Input('yaxis', 'value')]
        self.app.callback(Output("example-graph", "figure"), inputs)(self.updateGraphFromWebsite)

    def run(self):
        self.runFunc()

    def updateGraph(self):
        data = Interfaces.TensorflowGrid(self.model, self.x, self.y, self.df)
        data = Colorizers.Binary(data, highcontrast=self.highcontrast)
        self.fig = Graphs.PlotlyGrid(data, self.x, self.y)
        self.fig.update_layout(template=self.figtemplate)
        return self.fig

    def updateGraphFromWebsite(self, x, y):
        self.x = x
        self.y = y
        return self.updateGraph()

@VBSingletonProcess
def visualize(model, data: pd.DataFrame, title:str = "DashModelVisualizer", theme:str = "dark", folder = None,
              highcontrast:bool = True, notebook:bool = False, kagglenotebook:bool = False, mode:str = 'external',
              host:str = '0.0.0.0', port: bool = None):
    """
    Creates a dash website to visualize an ML model.

    :param model: A tensorflow keras model
    :param data: A pandas dataframe, all df columns must be numerical model inputs
    :param title: Title for website
    :param theme: Theme to load app in, can be a string (light / dark) or a url to load a stylesheet from
    :param folder: Directory to load additional css and js from
    :param highcontrast: Visualizes the model with orange and blue instead of green and red. Great for colorblind people!
    :param notebook: Uses jupyter dash instead of dash
    :param kagglenotebook: Enables ngrok tunneling for use in kaggle notebooks
    :param mode: Use 'external', 'inline', or 'jupyterlab'
    :param host: default hostname for dash
    :param port: None for default port (8050) or (1005)
    """
    print("Hello from inside visualization function.")
    from sys import stdout
    stdout.write("Hello from stdout\n")
    App(model, data, title, theme, folder, highcontrast, notebook, kagglenotebook, mode, host, port).run()