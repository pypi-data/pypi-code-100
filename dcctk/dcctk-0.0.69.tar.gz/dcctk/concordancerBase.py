import re
import math
import json
import cqls
from typing import Callable
from itertools import chain
from collections import Counter
from .UtilsConcord import queryMatchToken, match_mode
from .corpus import IndexedCorpus


class ConcordancerBase(IndexedCorpus):
    """Retrive concordance lines from the corpus with Corpus Query Language
    """

    _cql_default_attr = "char"
    _cql_max_quantity = 5
    all_idx_cache = None

    def cql_search(self, cql: str, left=5, right=5):
        """Search the corpus with Corpus Query Language

        Parameters
        ----------
        cql : str
            A CQL query
        left : int, optional
            Left context size, by default 5
        right : int, optional
            Right context size, by default 5

        Yields
        -------
        dict
            A dictionary with the structure:

            .. code-block:: python

                {
                    'left': [<tk>, <tk>, ...],
                    'keyword': [<tk>, <tk>, ...],
                    'right': [<tk>, <tk>, ...],
                    'position': ( <int>, <int>, <int>, <int> ),
                    'captureGroups': {
                        'verb': [<tk>],
                        'noun': [<tk>]}
                }

            where ``<tk>`` is a token (char), represented as a string,
        """
        queries = cqls.parse(
            cql, default_attr=self._cql_default_attr, max_quant=self._cql_max_quantity)

        for query in queries:
            for result in self._kwic(keywords=query, left=left, right=right):
                yield result

    def _kwic(self, keywords: list, left=5, right=5):
        # Get concordance from corpus
        search_results = self._search_keywords(keywords)
        if search_results is None:
            return []
        for subcorp_idx, text_idx, sent_idx, tk_idx in search_results:
            cc = self._kwic_single(subcorp_idx, text_idx, sent_idx, tk_idx, tk_len=len(
                keywords), left=left, right=right, keywords=keywords)
            yield ConcordLine(cc)

    def _kwic_single(self, subcorp_idx, text_idx, sent_idx, tk_idx, tk_len=1, left=5, right=5, keywords: list = None):
        # Flatten doc sentences to a list of tokens
        doc = self._get_corp_data(subcorp_idx, text_idx)
        text, keyword_idx = flatten_doc_to_sent(doc['c'])

        tk_start_idx = keyword_idx(sent_idx, tk_idx)
        tk_end_idx = tk_start_idx + tk_len
        start_idx = max(tk_start_idx - left, 0)
        end_idx = min(tk_end_idx + right, len(text))

        # Get CQL labeled token positions
        captureGroups = {}
        for i, keyword in enumerate(keywords):
            if '__label__' in keyword:
                for lab in keyword.get('__label__'):
                    if lab not in captureGroups:
                        captureGroups[lab] = {
                            's': '',
                            'i': [i, i]
                        }
                    tk = self._get_corp_data(
                        subcorp_idx, text_idx, sent_idx, i + tk_idx)
                    captureGroups[lab]['s'] += tk
                    captureGroups[lab]['i'][-1] = i

        return {
            "left": text[start_idx:tk_start_idx],
            "keyword": text[tk_start_idx:tk_end_idx],
            "right": text[tk_end_idx:end_idx],
            "position": (subcorp_idx, text_idx, sent_idx, tk_idx),
            "meta": {
                'id': self.corpus[subcorp_idx]['text'][text_idx]['id'],
                'time': self.get_meta(subcorp_idx, include_id=False),
                'text': self.get_meta(subcorp_idx, text_idx, include_id=False)
            },
            "captureGroups": captureGroups
        }

    def _search_keywords(self, keywords: list):
        #########################################################
        # Find keywords with the least number of matching results
        #########################################################
        best_search_loc = (0, None, math.inf)
        for i, keyword in enumerate(keywords):
            # Skip regex searches
            has_regex = False
            chars = keyword.get('match', {}).get(self._cql_default_attr, []) + \
                keyword.get('not_match', {}).get(self._cql_default_attr, [])
            for char in chars:
                if match_mode(char)[1] == 'regex':
                    has_regex = True
                    break
            if has_regex or len(chars) == 0: continue

            results = self._search_keyword(keyword)
            num_of_matched = len(results)
            if num_of_matched == 0:
                return None
            elif num_of_matched < best_search_loc[-1]:
                best_search_loc = (i, results, num_of_matched)
        results = best_search_loc[1]
        if results is None:
            results = self._search_keyword(keyword)

        #######################################
        # Check other tokens around search seed
        #######################################
        keyword_anchor = {
            'length': len(keywords),
            'seed_idx': best_search_loc[0]
        }

        # Check all possible matching keywords
        matched_results = []
        for idx in results:
            # Get all possible matching keywords from corpus
            candidates = self._get_keywords(keyword_anchor, *idx)
            if len(candidates) != len(keywords):
                continue
            # Check every token in keywords
            matched_num = 0
            for w_k, w_c in zip(keywords, candidates):
                if queryMatchToken(queryTerm=w_k, corpToken=w_c):
                    matched_num += 1
            if matched_num == len(keywords):
                first_keyword_idx = idx[3] - keyword_anchor['seed_idx']
                matched_results.append(
                    [idx[0], idx[1], idx[2], first_keyword_idx])

        return matched_results

    def _search_keyword(self, keyword: dict):
        """Global search of a keyword to find candidates of correct kwic instances

        Parameters
        ----------
        keyword : dict
            A dictionary specifying the matching conditions of
            the keyword:

            .. code-block:: python

                {
                    'match': {
                        'word': ['打'],
                        'pos': ['V.*']
                    }, 
                    'not_match': {
                        'pos': ['VH.*']
                    },
                    '__label__': ['l1']  #labels to attached to search results  
                }

        Returns
        -------
        list
            A list of matching indicies
        """
        positive_match = set()
        negative_match = set()

        # Deal with empty token {}
        if ('match' not in keyword) and ('not_match' not in keyword):
            if self.all_idx_cache is None:
                self.all_idx_cache = set(chain.from_iterable(self.index.values()))
            return self.all_idx_cache
        else:
            ########################################
            ##########   POSITIVE MATCH   ##########
            ########################################
            matching_idicies = Counter()
            chars = keyword['match'].get(self._cql_default_attr, [])
            for idx in self._intersect_search(chars):
                matching_idicies.update({idx: 1})

            # Get indicies that matched all given tags
            for idx, count in matching_idicies.items():
                if count == len(keyword['match']):
                    positive_match.add(idx)

            # Special case: match is empty
            if len(keyword['match']) == 0:
                if self.all_idx_cache is None:
                    self.all_idx_cache = set(chain.from_iterable(self.index.values()))
                positive_match = self.all_idx_cache

            ########################################
            ##########   NEGATIVE MATCH   ##########
            ########################################
            chars = keyword['not_match'].get(self._cql_default_attr, [])
            for idx in self._union_search(chars):
                negative_match.add(idx)

            ########################################
            #####  POSITIVE - NEGATIVE MATCH  ######
            ########################################
            positive_match.difference_update(negative_match)

        if len(positive_match) == 0:
            print(f"{keyword} not found in corpus")

        return positive_match


    def _union_search(self, values: list):
        """Given candidates values, return from corpus the 
        position of tokens matching any of the values.

        Parameters
        ----------
        values : list
            A list of values to compare with
        """
        matched_indicies = set()

        for value in values:
            value, mode = match_mode(value)
            if mode == "literal":
                matched_indicies.update(self.index.get(value, []))
            else:
                for char in self.index:
                    if re.search(value, char):
                        matched_indicies.update(self.index[char])

        return matched_indicies

    def _intersect_search(self, values: list):
        """Given candidates values, return from corpus the
        position of tokens matching all values.

        Parameters
        ----------
        values : list
            A list of values to compare with
        """
        # Get intersections of all values
        match_count = Counter()
        for value in values:
            value, mode = match_mode(value)
            indices = set()
            if mode == "literal":
                indices = self.index.get(value, set())
            else:
                for char in self.index:
                    if re.search(value, char):
                        indices.update(self.index[char])

            for idx in indices:
                match_count.update({idx: 1})

        # Filter idicies that match all values given
        intersect_match = set()
        for idx, count in match_count.items():
            if count == len(values):
                intersect_match.add(idx)

        return intersect_match

    def _get_keywords(self, search_anchor: dict, subcorp_idx, doc_idx, sent_idx, tk_idx):
        sent = self._get_corp_data(subcorp_idx, doc_idx, sent_idx)
        start_idx = max(0, tk_idx - search_anchor['seed_idx'])
        end_idx = min(start_idx + search_anchor['length'], len(sent))

        return sent[start_idx:end_idx]

    def _get_corp_data(self, subcorp_idx, doc_idx=None, sent_idx=None, tk_idx=None):
        """Get corpus data by position
        """
        if doc_idx is None:
            return self.corpus[subcorp_idx]
        if sent_idx is None:
            return self.corpus[subcorp_idx]['text'][doc_idx]
        if tk_idx is None:
            return self.corpus[subcorp_idx]['text'][doc_idx]['c'][sent_idx]
        return self.corpus[subcorp_idx]['text'][doc_idx]['c'][sent_idx][tk_idx]


class ConcordLine:

    def __init__(self, cc: dict):
        """Initialize an instance of concordance line

        Parameters
        ----------
        cc : dict
            A dictionary returned by
            :meth:`concordancer.Concordancer._kwic_single`.
            It has the following stucture:

            .. code-block:: python

                {
                    'left': '，又喜',
                    'keyword': '將軍之去，',
                    'right': '計必乘',
                    'position': (2, 55, 5, 208),
                    'meta': {
                        'id': '03/三國志_蜀書七.txt',
                        'time': {
                            'time_range': [221, 589], 
                            'label': '魏晉南北', 
                            'ord': 3
                        },
                        'text': {
                            'book': '三國志', 'sec': '蜀書七'
                        }
                    },
                    'captureGroups': {
                        'obj': {'s': '去，', 'i': [3, 4]}
                    }
                }
        """
        self.data = cc
        self.meta = obj(**cc.get('meta'))
    

    def __repr__(self) -> str:
        l, k, r = self.data['left'], self.data['keyword'], self.data['right']
        cc = '<Concord ' + l + '{' + k + '}' + r + '>'
        return cc


    def get_kwic(self, return_keyword_idx=True):
        """Get string representation of the concordance line

        Parameters
        ----------
        return_keyword_idx : bool, optional
            Whether to return the index of the keywords
            in the concordance line, by default True

        Returns
        -------
        str or tuple
            If return keyword_idx is True, returns tuple,
            with the second element being the index of the
            keywords (idx_from, idx_to).
        """
        l, k, r = self.data['left'], self.data['keyword'], self.data['right']
        s = l + k + r
        if return_keyword_idx:
            i_fr = len(l)
            i_to = i_fr + len(k) - 1
            return s, (i_fr, i_to)
        return s        


    def get_timestep(self, key:Callable=None):
        """Get time step info of the concordance line

        Parameters
        ----------
        key : Callable, optional
            If specified, applied on self.meta.time to return
            time step data. By default None, which uses 
            subcorp_idx as time step information.

        Returns
        -------
        Int
            The time step that the concordance line belongs to.
        """
        if key is not None:
            return key(self.meta.time)
        return self.data['position'][0]


    def to_json(self, ensure_ascii=False, indent=False):
        return json.dumps(self.data, ensure_ascii=ensure_ascii, indent=indent)



class obj(object):
    def __init__(self, **entries):
        self.__dict__.update(entries)
    
    def __repr__(self):
        s = []
        for k, v in self.__dict__.items():
            s.append(f".{k} = {str(v)}")
        return '\n'.join(s)

##################
# Helper functions
##################
def flatten_doc_to_sent(doc):
    text = ''
    sent_lengths = []
    for sent in doc:
        sent_lengths.append(len(sent))
        text += sent

    def keyword_idx(sent_idx, tk_idx):
        nonlocal sent_lengths
        for i in range(sent_idx):
            tk_idx += sent_lengths[i]
        return tk_idx

    return text, keyword_idx
