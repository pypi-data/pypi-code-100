import pandas as pd
from itertools import chain
from collections import Counter
from typing import Union, Sequence
from .corpus import IndexedCorpus
from .dispersionStats import Range, DP, DPnorm, KLdivergence, JuillandD, RosengrenS


class Dispersion(IndexedCorpus):
    
    def __init__(self, corpus) -> None:
        IndexedCorpus.__init__(self, corpus)

        # Corpus sizes
        self.num_of_subcorp = len(self.corpus)
        self.corp_size = 0
        self.subcorp_size = [ 0 ] * self.num_of_subcorp
        self.text_size = {}
        self.num_of_text = 0
        self.num_of_text_in_each_subcorp = [ 0 ] * self.num_of_subcorp
        self._compute_sizes()
        # Free memory
        del self.corpus

        # Functions for measures of dispersion
        self.dispersion_func = [ 
            Range, DP, DPnorm, KLdivergence, JuillandD, RosengrenS
        ]


    def pattern_dispersion(self, data:Union[pd.DataFrame, Sequence], subcorp_idx:int=None, return_raw=False):
        """Compute dispersion measures of a complex pattern

        Parameters
        ----------
        data : Union[pd.DataFrame, Sequence]
            Data returned by :meth:`concordancer.Concordancer.cql_search` 
            (i.e., a sequence/generator of :class:`concordancer.ConcordLine`) 
            or :class:`pandas.DataFrame` with a column :code:`m.id` specifying
            the path to a text file (i.e., a dataframe recording the clustering 
            result of :meth:`concordSimil.ConcordSimil.hierarchical_clustering`).
        subcorp_idx : int, optional
            The index of the subcorpus used to derive the data, 
            by default None, which uses the full corpus to derive 
            the data.
        return_raw : bool, optional
            Whether to return the data used for computing 
            dispersion statisitcs, by default False

        Returns
        -------
        dict or tuple
            A dictionary recording various dispersion measures.
            If :code:`return_raw` is True, an additional dictionary
            recording data used for computing dispersion measures 
            is returned.
        """

        if isinstance(data, pd.DataFrame):
            v = Counter(self.path_index[p] for p in data['m.id'])
        else:
            v = Counter(c.data['position'][:2] for c in data)
        return self._compute_dispersion(v, subcorp_idx, return_raw)


    def char_dispersion(self, char:str, subcorp_idx:int=None, return_raw=False):
        """Compute dispersion measures of a character

        Parameters
        ----------
        char : str
            The target character
        subcorp_idx : int, optional
            The index of the subcorpus used to derive the data, 
            by default None, which uses the full corpus to derive 
            the data.
        return_raw : bool, optional
            Whether to return the data used for computing 
            dispersion statisitcs, by default False

        Returns
        -------
        dict or tuple
            A dictionary recording various dispersion measures.
            If :code:`return_raw` is True, an additional dictionary
            recording data used for computing dispersion measures 
            is returned.
        """
        v = Counter((i, j) for i, j, _, _ in self.index.get(char, []))
        if len(v) == 0:
            print(f'No instances of `{char}` found in the corpus!')
        return self._compute_dispersion(v, subcorp_idx, return_raw)


    def _compute_dispersion(self, v, subcorp_idx, return_raw):
        d = self._get_dispersion_data(v, subcorp_idx)
        stats = { func.__name__: func(d) for func in self.dispersion_func }
        if return_raw:
            return stats, d
        else:
            return stats
    

    def _get_dispersion_data(self, v:Union[Counter, dict], subcorp_idx:int=None):
        """Get data from calculating dispersion statistics

        Parameters
        ----------
        v : Union[Counter, dict]
            A counter with keys in the form of :code:`(<subcorp_idx>, <text_idx>)`
            specifying a text and values raw frequencies of a particular pattern 
            in this text.
        subcorp_idx : int, optional
            The index of the subcorpus used to derive the data, 
            by default None, which uses the full corpus to derive 
            the data.

        Returns
        -------
        dict
            A dictionary of parameters for calculating dispersion stats

        Notes
        -----
        See page 102 in [1] for details of the definitions of the returned data

        References
        ----------
        [1] Gries (2020). Analyzing dispersion. In M. Paquot & S. Th. Gries (Eds.),
        A practical handbook of corpus linguistics (pp. 99–118). Cham: Springer 
        International Publishing. https://doi.org/10.1007/978-3-030-46216-1_5
        """

        if isinstance(subcorp_idx, int):
            corp_size = self.subcorp_size[subcorp_idx]
            size = self.num_of_text_in_each_subcorp[subcorp_idx]
            V = [ 0 ] * size
            P = V.copy()
            S = V.copy()
            for j in self.text_size[subcorp_idx]:
                Vj = v.get((subcorp_idx, j), 0)
                Pj = Vj / self.text_size[subcorp_idx][j]['r']
                Sj = self.text_size[subcorp_idx][j]['s']
                V[j], P[j], S[j] = Vj, Pj, Sj
        else:
            corp_size = self.corp_size
            size = self.num_of_text
            V = [ 0 ] * size
            P = V.copy()
            S = V.copy()
            c = 0
            for i in self.text_size:
                for j in self.text_size[i]:
                    Vj = v.get((i, j), 0)
                    Pj = Vj / self.text_size[i][j]['r']
                    Sj = self.text_size[i][j]['t']
                    V[c], P[c], S[c] = Vj, Pj, Sj
                    c += 1
        return {
                'n': size,
                'v': V,
                'p': P,
                's': S,
                'f': sum(V),
                'corpus_size': corp_size 
        }


    def _compute_sizes(self):
        for i in range(self.num_of_subcorp):
            subcorp_size = 0
            if i not in self.text_size:
                self.text_size[i] = {}
            for j, text in enumerate(self.corpus[i]['text']):
                self.text_size[i][j] = {
                    'r': sum(len(sent) for sent in text.get('c', [])),
                    's': 0.0,
                    't': 0.0,
                }
                subcorp_size += self.text_size[i][j]['r']
            self.subcorp_size[i] = subcorp_size
        self.corp_size = sum(self.subcorp_size)
        self.num_of_text = len(list(chain.from_iterable(self.text_size.values())))

        # Get relative freq
        for i in self.text_size:
            for j in self.text_size[i]:
                self.text_size[i][j]['s'] = self.text_size[i][j]['r'] / self.subcorp_size[i]
                self.text_size[i][j]['t'] = self.text_size[i][j]['r'] / self.corp_size

                self.num_of_text_in_each_subcorp[i] += 1
