from MLVisualizationTools import Analytics, Interfaces, Graphs, Colorizers
from MLVisualizationTools.backend import fileloader
import pandas as pd
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # stops agressive error message printing
from tensorflow import keras

try:
    import matplotlib.pyplot
except ImportError:
    raise ImportError("Matplotlib is required to run this demo. If you don't have matplotlib installed, install it"
                      " with `pip install matplotlib` or run the plotly demo instead.")

def main():
    model = keras.models.load_model(fileloader('examples/Models/titanicmodel'))
    df: pd.DataFrame = pd.read_csv(fileloader('examples/Datasets/Titanic/train.csv'))

    AR = Analytics.Tensorflow(model, df, ["Survived"])
    maxvar = AR.maxVariance()

    grid = Interfaces.TensorflowGrid(model, maxvar[0].name, maxvar[1].name, df, ["Survived"])
    grid = Colorizers.Simple(grid, 'red')
    plt, _, _ = Graphs.MatplotlibGrid(grid, maxvar[0].name, maxvar[1].name, title="Max Variance")
    plt.show(block=False)

    grid = Interfaces.TensorflowGrid(model, 'Parch', 'SibSp', df, ["Survived"])
    grid = Colorizers.Binary(grid, highcontrast=True)
    plt, _, _ = Graphs.MatplotlibGrid(grid, 'Parch', 'SibSp', title="Parch by SibSp")
    plt.show()

if __name__ == "__main__":
    main()