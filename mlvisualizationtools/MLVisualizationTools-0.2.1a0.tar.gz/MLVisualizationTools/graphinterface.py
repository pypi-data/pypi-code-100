#We use just-in-time importing here to improve load times
#Here are the imports:
#import plotly.express as px
#import matplotlib.pyplot as plt
import pandas as pd


def plotlyGrid(data: pd.DataFrame, x: str, y: str, output="Output", title=""):
    """
    Calls px.scatter_3d with data. Returns a plotly figure.

    :param data: pandas dataframe with cols x, y, and output. Color is optional
    :param x: xcol in df
    :param y: ycol in df
    :param output: zcol in df
    :param title: Title for graph
    """
    try:
        import plotly.express as px
    except:
        raise Exception("Plotly is required to use this graph. Install with `pip install plotly`")
    if "Color" in data:
        color = "Color"
        colormap = "identity"
    else:
        color = None
        colormap = None
    fig = px.scatter_3d(data, x, y, output, color=color, color_discrete_map=colormap, title=title)
    return fig

def plotlyAnimation(data, x, y, anim, output="Output", title=""):
    """
    Calls px.scatter_3d with data and animation frame. Returns a plotly figure.

    :param data: pandas dataframe with cols x, y, anim, and output. Color is optional
    :param x: xcol in df
    :param y: ycol in df
    :param anim: column for animation
    :param output: zcol in df
    :param title: Title for graph
    """
    try:
        import plotly.express as px
    except:
        raise Exception("Plotly is required to use this graph. Install with `pip install plotly`")
    if "Color" in data:
        color = "Color"
        colormap = "identity"
    else:
        color = None
        colormap = None

    fig = px.scatter_3d(data, x, y, output, animation_frame=anim, color=color, color_discrete_map=colormap,
                        title=title, range_z=[data[output].min(), data[output].max()])
    return fig

def matplotlibGrid(data, x, y, output="Output", title=""):
    """
    Calls ax.scatter with data. Returns a plt instance, a fig, and the ax.

    :param data: pandas dataframe with cols x, y, and output. Color is optional
    :param x: xcol in df
    :param y: ycol in df
    :param output: zcol in df
    :param title: Title for graph
    """
    try:
        import matplotlib.pyplot as plt
    except:
        raise Exception("Matplotlib is required to use this graph. Install with `pip install matplotlib`")
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    if "Color" in data:
        color = data["Color"]
    else:
        color = None

    ax.scatter(data[x], data[y], data[output], c=color)
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_zlabel(output)
    ax.set_title(title)

    return plt, fig, ax