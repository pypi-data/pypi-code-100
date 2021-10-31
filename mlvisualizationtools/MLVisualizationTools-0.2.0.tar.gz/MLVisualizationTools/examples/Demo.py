from MLVisualizationTools import Analytics, Interfaces, Graphs, Colorizers
from MLVisualizationTools.backend import fileloader
import pandas as pd
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' #stops agressive error message printing
from tensorflow import keras

try:
    import plotly
except:
    raise ImportError("Plotly is required to run this demo. If you don't have plotly installed, install it with"
                      " `pip install plotly' or run the matplotlib demo instead.")

def main():
    model = keras.models.load_model(fileloader('examples/Models/titanicmodel'))
    df: pd.DataFrame = pd.read_csv(fileloader('examples/Datasets/Titanic/train.csv'))

    AR = Analytics.Tensorflow(model, df, ["Survived"])
    maxvar = AR.maxVariance()

    grid = Interfaces.TensorflowGrid(model, maxvar[0].name, maxvar[1].name, df, ["Survived"])
    grid = Colorizers.Binary(grid)
    fig = Graphs.PlotlyGrid(grid, maxvar[0].name, maxvar[1].name)
    fig.show()

    grid = Interfaces.TensorflowGrid(model, 'Parch', 'SibSp', df, ["Survived"])
    grid = Colorizers.Binary(grid, highcontrast=True)
    fig = Graphs.PlotlyGrid(grid, 'Parch', 'SibSp')
    fig.show()

main()