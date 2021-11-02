from MLVisualizationTools.express import DashModelVisualizer
from MLVisualizationTools.backend import fileloader
import pandas as pd
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' #stops agressive error message printing
from tensorflow import keras

def main(theme = 'dark', highcontrast = True):
    """
    Runs the demo by calling DashModelVisualizer

    :param theme: theme, could be 'light' or 'dark'
    :param highcontrast: Use blue and orange coloring instead of red and green
    """
    model = keras.models.load_model(fileloader('examples/Models/titanicmodel'))
    df: pd.DataFrame = pd.read_csv(fileloader('examples/Datasets/Titanic/train.csv'))
    df = df.drop("Survived", axis=1)
    DashModelVisualizer.visualize(model, df, title="DashInteractiveDemo", theme=theme,
                                  highcontrast=highcontrast)

print("This demo is for use outside of a jupyter notebook and uses the default precompiled model.")
print("To run the demo, call DashDemo.main()")
if __name__ == "__main__":
    main()