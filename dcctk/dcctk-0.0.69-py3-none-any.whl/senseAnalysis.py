import pandas as pd
from copy import deepcopy


class SenseAnalysis:
    """Sense distribution based on sense clustering of concordance lines
    """

    sense_distribution = None
    sense_distribution_raw = None
    ts_label_map = []
    """Timestep meta info
    """

    def __init__(self, CS):
        """Initialize sense analysis

        Parameters
        ----------
        CS : ConcordSimil
            An instance of :class:`concordSimil.ConcordSimil` where 
            hierarchical clustering has been performed on.
        """
        self._embeddings = CS.embeddings
        self._embeddings_plotting = CS.embeddings_plotting
        self.df = CS.hover_df

        if 'cluster' not in self.df:
            raise Exception(f'Clustering not performed yet, please run `.hierarchical_clustering()` in {CS} before passing it in.')

        # Sense distribution
        self._sense_distribution_across_time()
    
    
    def plot_sense_distribution(self, timelabel:str=None, **kwargs):
        """Plot distribution of sense clusters across time

        Parameters
        ----------
        timelabel : str, optional
            Key specifying the label to use on the x-axis. Avaliable labels
            are found in :attr:`SenseAnalysis.ts_label_map`. By default None.
        """
        ax = self.sense_distribution.plot.bar(**kwargs)
        if timelabel is None:
            ax.set_xticklabels(list(range(len(self.ts_label_map))), rotation=0)
        else:
            ax.set_xticklabels([l[timelabel] for l in self.ts_label_map], rotation=0)


    def plot_sense_timeseries(self, clusters:list=None, timelabel:str=None, raw_count=True, **kwargs):
        d = deepcopy(self.sense_distribution_raw)
        if not raw_count:
            total_freq = d.apply(lambda x: x.sum(), axis=0)
            d = d / total_freq

        # Subset
        if clusters is not None:
            d = d[ [int(x) for x in clusters] ]
        if timelabel is not None:
            d['label'] = [l[timelabel] for l in self.ts_label_map]
        else:
            d['label'] = [ str(i) for i in range(len(self.ts_label_map)) ]

        ax = d.plot.line(x='label', **kwargs)  # cmap=plt.cm.get_cmap('Reds', d.shape[1])
        ax = ax.set_xlabel('')


    def _sense_distribution_across_time(self):
        # Get frequency distributions
        distr = {}  
        num_of_ts = len(set(self.df.timestep))
        self.ts_label_map = [0] * num_of_ts
        time_meta_labels = self.df.columns[self.df.columns.to_series().str.contains('m.time')]
        for idx, row in self.df.iterrows():
            c = row['cluster']
            ts = int(row['timestep'])
            
            # Get distribution
            if c not in distr:
                distr[c] = [0] * num_of_ts
            distr[c][ts] += 1

            # Get timestep info
            if isinstance(self.ts_label_map[ts], int):
                self.ts_label_map[ts] = dict(row[time_meta_labels])

        d = pd.DataFrame(distr)
        d = d.reindex(sorted(d.columns), axis=1)
        self.sense_distribution_raw = deepcopy(d)
        total_freq = d.apply(lambda x: x.sum(), axis=1)
        for index, row in d.iterrows(): 
            d.loc[index] = row / total_freq[index]
        self.sense_distribution = d
