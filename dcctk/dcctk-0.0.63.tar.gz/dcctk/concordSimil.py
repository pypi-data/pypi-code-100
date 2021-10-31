import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Callable
from tqdm.auto import trange
from .UtilsGeneral import stringify_obj, flatten
from .UtilsStats import cossim

class ConcordSimil:
    """Similarity analysis of concordance lines
    """

    def __init__(self, concord_lines, bert_model, is_traditional=True, 
        token_idx:tuple=None):
        """Initialize similarity analysis

        Parameters
        ----------
        concord_lines : Sequence
            A sequence of :class:`dcctk.concordancer.ConcordLine`.
        bert_model : AnchiBert
            An intialized :class:`dcctk.embeddings.AnchiBert`. Alternatively,
            one can write a custom class that has a method 
            :code:`encode_sentence`, as in 
            :meth:`dcctk.embeddings.AnchiBert.encode_sentence`.
        is_traditional : bool, optional
            Whether to use :meth:`opencc.Opencc.convert` to translate tradional
            Chinese into simplified Chinese, by default True, which uses the
            :code:`t2s.json` configuration.
        """
        
        self.model = bert_model
        self.concords = concord_lines
        self.concords_len = len(self.concords)
        self.embeddings = np.empty((self.concords_len, 768))
        self._get_embeddings(is_traditional, token_idx)
        self.embeddings_plotting = None
        self.clustering = None

        # Plotting info
        hover_df = []
        for i, x in enumerate(self.concords):
            d = {
                'left': x.data['left'],
                'keyword': x.data['keyword'],
                'right': x.data['right'],
                'timestep': x.get_timestep(),
            }
            for k, v in flatten(x.data['meta'], parent_key='m').items():
                d[k] = stringify_obj(v)
            d['emb_id'] = i
            hover_df.append(d)
        self.hover_df = pd.DataFrame(hover_df)
    

    def __repr__(self) -> str:
        return f"<ConcordSimil  clustered: {'cluster' in self.hover_df}>"


    def hierarchical_clustering(self, threshold=5, criterion='maxclust', standardize_features=True, method='average', metric='cosine', visualize=True):
        """Hierarchical clustering of concordance lines
        """
        from scipy.cluster.hierarchy import fcluster

        if self.clustering is None:
            self.hierarchical_clustering_explore(method=method, metric=metric, standardize_features=standardize_features, dendrogram=False, elbow=False)
        self.hover_df['cluster'] = fcluster(self.clustering, t=threshold, criterion=criterion)

        if visualize:
            self.plot_cluster_results()

        return self.hover_df
    

    def plot_cluster_results(self, interactive=False, labels='cluster', **keywords):
        if labels not in self.hover_df:
            Warning('Clustering not performed yet, please run `ConcordSimil.hierarchical_clustering()` before calling this function.')
            return
        self.plot_embeddings(interactive=interactive, labels=labels, **keywords)


    def hierarchical_clustering_explore(self, method='average', metric='cosine', \
        standardize_features=True, dendrogram=True, elbow=True,
        elbow_metrics="distortion calinski_harabasz silhouette", figsize=(23,7)):
        """Perform hierarchical clustering on the embedding space

        Parameters
        ----------
        standardize_features : bool, optional
            Whether to use zscores for each of the 768 dimension in the 
            Bert model, by default True
        """
        from scipy.stats import zscore
        from scipy.cluster.hierarchy import linkage

        # Scale features
        if standardize_features:
            X = zscore(self.embeddings, axis=0)
        else:
            X = self.embeddings
        
        # Clustering with cosine distance and average linkage method
        self.clustering = linkage(X, method=method, metric=metric)
        # Dendrogram
        if dendrogram:
            self.plot_dendrogram(figsize=figsize)
        
        # Elbow visualizer
        if elbow:
            from sklearn.cluster import AgglomerativeClustering
            model = AgglomerativeClustering(linkage=method, affinity=metric)
            self.plot_elbow(model, X, metrics=elbow_metrics, figsize=figsize)


    def plot_elbow(self, cluster_model, data, metrics='distortion calinski_harabasz silhouette', figsize=(23, 7)):
        from yellowbrick.cluster import KElbowVisualizer
        
        # Plot
        metrics = metrics.strip().split()
        fig, axes = plt.subplots(ncols=len(metrics), figsize=figsize)
        for i, m in enumerate(metrics):
            visualizer = KElbowVisualizer(cluster_model, k=(2,30), metric=m, timings= False, locate_elbow=True, ax=axes[i])
            visualizer.fit(data)      # Fit the data to the visualizer
            visualizer.finalize()  # Finalize and render the figure


    def plot_dendrogram(self, model=None, figsize=(25,10)):
        from scipy.cluster.hierarchy import dendrogram
        
        fig = plt.figure(figsize=figsize)
        if model is None:
            dn = dendrogram(self.clustering)
        else:
            dn = dendrogram(model)
        plt.show()


    def plot_embeddings(self, interactive=True, labels:str=None, **keywords):
        import umap.plot
        if self.embeddings_plotting is None:
            self.embeddings_plotting = self.embeddings_dim_reduce(dim=2, method="umap")
        labels = self.hover_df[labels] if labels is not None else None

        if interactive:
            from bokeh.plotting import show as bokeh_show
            f = umap.plot.interactive(self.embeddings_plotting, 
                            labels=labels, 
                            hover_data=self.hover_df, 
                            **keywords)
            bokeh_show(f)
        else:
            umap.plot.points(self.embeddings_plotting, labels=labels, **keywords)


    def embeddings_dim_reduce(self, dim=2, method="umap"):
        print(f"Reducing the embedding space to {dim} dimensions...")
        if method.lower() == "umap":
            import umap
            emb = umap.UMAP(n_components=dim, metric='cosine').fit(self.embeddings)
        if method.lower() == "pca":
            from sklearn.decomposition import PCA
            emb = PCA(n_components=dim).fit_transform(self.embeddings)
        return emb


    def semantic_sort(self, base_sent:str=None, base_tk:tuple=None, is_traditional=True, simil_func:Callable=cossim):
        """Sort concordance lines based on Bert vector similarities

        Parameters
        ----------
        base_sent : str, optional
            The sentence used to compare with, by default None,
            which takes the first element of :code:`concord_lines`
            as the base sentence.
        base_tk : tuple, optional
            A tuple of length 2, specifying the position 
            :code:`(idx_from, idx_to)` of the keywords in
            :code:`base_sent`, by default None. If None, the
            vector is computed from summing up all token vectors in the sentence.
        is_traditional : bool, optional
            Whether to convert traditional into simplified Chinese
            before feeding the input to AnchiBert, by default True.
            This parameter is passed to 
            :meth:`dcctk.embeddings.AnchiBert.encode_sentence`.
        simil_func : Callable, optional
            Function for computing similarity between two vectors,
            by default :func:`dcctk.UtilsStats.cossim`. The function 
            should take the input vectors as its two arguments and
            returns a float.

        Returns
        -------
        list
            A list of 2-tuples :code:`(<ConcordLine>, <float>)`, 
            with the second elements being the similarity scores
            to :code:`base_sent (base_tk)`.
        """
        if base_sent is None:
            base_sent, base_tk = self.concords[0].get_kwic()
        
        if base_tk is not None:
            compare_base = self.model.encode_sentence(base_sent, *base_tk, is_traditional=is_traditional)
        else:
            compare_base = self.model.encode_sentence(base_sent, is_traditional=is_traditional)

        results = []
        for i in trange(len(self.concords)):
            results.append( (self.concords[i], simil_func(compare_base, self.embeddings[i])) )

        return sorted(results, key=lambda x: x[1], reverse=True)


    def _get_embeddings(self, is_traditional=True, token_idx:tuple=None):
        """Pre-compute embeddings from Bert model

        Parameters
        ----------
        is_traditional : bool, optional
            Whether to convert traditional into simplified Chinese
            before feeding the input to AnchiBert, by default True.
            This parameter is passed to 
            :meth:`dcctk.embeddings.AnchiBert.encode_sentence`.
        token_idx : tuple, optional
            A tuple of length 2, specifying the position 
            :code:`(idx_from, idx_to)` of the keywords in
            :code:`base_sent`, by default None. If None, the
            vector is computed from summing up all token vectors in the sentence.
        """
        print('Computing bert embeddings...')
        for i in trange(self.concords_len):
            sent, tk_idx = self.concords[i].get_kwic()
            if token_idx is not None:
                tk_idx = token_idx
            self.embeddings[i] = self.model.encode_sentence(sent, *tk_idx, is_traditional=is_traditional)
