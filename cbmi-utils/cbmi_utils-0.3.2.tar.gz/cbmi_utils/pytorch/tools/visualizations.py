import matplotlib.pyplot as plt
import numpy as np
import seaborn
import umap
from sklearn.manifold import TSNE
from sklearn.metrics import confusion_matrix


def create_umap_plot(data: np.array, targets: np.array = None, reducer_seed: int = 42):
    reducer = umap.UMAP(random_state=reducer_seed)
    mapper = reducer.fit(data)
    umap_plot = umap.plot.points(mapper, labels=targets, theme='fire')
    return umap_plot.figure


def create_conf_matrix_plot(data: np.array, targets: np.array, plot_labels='auto'):
    conf_matrix = confusion_matrix(data, targets, normalize='all')
    conf_plot = seaborn.heatmap(conf_matrix, annot=True, cmap="Blues",
                                xticklabels=plot_labels, yticklabels=plot_labels)
    plt.tight_layout()
    return conf_plot.figure


def UMAP_vis(feature_vector_arr, label_vector_arr, set_name=None):

    scaled_data = StandardScaler().fit_transform(feature_vector_arr)

    reducer = umap.UMAP()
    embedding = reducer.fit_transform(scaled_data)

    fig = plt.figure(figsize=(10, 10))
    plt.scatter(
        embedding[:, 0],
        embedding[:, 1],
        s=3,
        c=[seaborn.color_palette()[int(x)] for x in label_vector_arr])
    plt.gca().set_aspect('equal', 'datalim')
    plt.grid()
    if set_name:
        plt.title('UMAP projection of the ('+set_name+') embedding', fontsize=18)
    else:
        plt.title('UMAP projection of the embedding', fontsize=18)

    return fig


def TSNE_vis(feature_vector_arr, label_vector_arr, set_name=None):
    embedding = TSNE(n_components=2).fit_transform(feature_vector_arr)

    fig = plt.figure(figsize=(10, 10))
    plt.scatter(
        embedding[:, 0],
        embedding[:, 1],
        s=3,
        c=[seaborn.color_palette()[int(x)] for x in label_vector_arr])
    plt.gca().set_aspect('equal', 'datalim')
    plt.grid()
    if set_name:
        plt.title('TSNE projection of the ('+set_name+') embedding', fontsize=18)
    else:
        plt.title('TSNE projection of the embedding', fontsize=18)

    return fig
