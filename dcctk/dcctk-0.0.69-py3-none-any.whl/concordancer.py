#%%
import cqls
from itertools import chain
from CompoTree import IDC
from collections import Counter

from .concordancerBase import ConcordancerBase, ConcordLine
from .subCharQuery import find_compo, load_lexicon, char_match_compo, get_radicals
from .UtilsConcord import queryMatchToken
from .UtilsSubchar import all_plain_cql, has_cql_match_type, is_subchar
from .UtilsStats import additive_smooth


class Concordancer(ConcordancerBase):
    
    lexicon = None

    def cql_search(self, cql: str, left=5, right=5):
        queries = cqls.parse(cql, default_attr=self._cql_default_attr, \
            max_quant=self._cql_max_quantity)
        
        # Cond0: all plain cql search
        if sum(all_plain_cql(q) for q in queries) == len(queries):
            for res in super(Concordancer, self).cql_search(cql, left, right):
                yield res
            return
        
        if self.lexicon is None:
            self.lexicon = load_lexicon(self.index.keys())

        for query in queries:
            # Cond1: has plain char match (plain char as anchor)
            if has_cql_match_type(query, "literal"):

                subchar_idx = [i for i, tk in enumerate(query) if is_subchar(tk)]
                query_pl = [q if i not in subchar_idx else {} \
                    for i, q in enumerate(query)]
                
                for result in self._kwic(keywords=query_pl, left=left, right=right):
                    candi = result.data['keyword']
                    matched_num = sum(1 for i in subchar_idx \
                        if char_match_compo(candi[i], query[i], self.lexicon, self.__hash__()) )
                    if matched_num == len(subchar_idx):
                        yield result
            
            # Cond2: no plain char match (compo as anchor)
            else:
                subchar_idx = [i for i, tk in enumerate(query) if is_subchar(tk)]
                tk0 = query[subchar_idx[0]]

                matched_chars = find_compo(tk0, self.lexicon, self.__hash__())

                len_query = len(query)
                keyword_anchor = {
                    'length': len_query,
                    'seed_idx': subchar_idx[0]
                }

                for idx in chain.from_iterable(self.index[c] for c in matched_chars):
                    candidates = self._get_keywords(keyword_anchor, *idx)
                    if len(candidates) != len_query: continue
                    # Check every token in keywords
                    matched_num = 0
                    for w_k, w_c in zip(query, candidates):
                        if is_subchar(w_k):
                            if char_match_compo(w_c, w_k, self.lexicon, self.__hash__()):
                                matched_num += 1
                        else: 
                            if queryMatchToken(queryTerm=w_k, corpToken=w_c):
                                matched_num += 1
                    if matched_num == len_query:
                        subcorp_idx, text_idx, sent_idx, tk_idx = \
                        idx[0], idx[1], idx[2], idx[3] - keyword_anchor['seed_idx']
                        cc = self._kwic_single(subcorp_idx, text_idx, sent_idx, tk_idx, \
                            tk_len=len_query, left=left, right=right, keywords=query)
                        yield ConcordLine(cc)
    

    @property
    def chr_idcs(self):
        return { x.name: x.value for x in IDC }

    @property
    def chr_radicals(self):
        if self.lexicon is None:
            self.lexicon = load_lexicon(self.index.keys())
        return get_radicals(self.lexicon)


    @property
    def cql_attrs(self):
        return {
            "Default": ['char'],
            "CharComponent": ['compo', 'max_depth', 'idc', 'pos'],
            "CharRadical": ['radical'],
            "CharPhonetic": {
                "moe": ['phon', 'tone', 'tp', 'sys="moe"'],
                "廣韻": [
                    '攝', '聲調', '韻母', '聲母', '開合', 
                    '等第', '反切', '拼音', 'IPA', 'sys="廣韻"'
                ]
            }
        }


    def collocates(self, node_cql:str, left=1, right=1, subcorp_idx=None, sort_by="Gsq", alpha=0.1, chinese_only=True):
        """
                     node       ~node
        collocate    O11         O12    R1 (char index len)
        ~collocate   O21         O22    R2
                      C1          C2   CorpSize
                   (Concord num)
        """
        o11 = Counter()
        C1 = 0
        for m in self.cql_search(node_cql, left, right):
            m = m.data
            if isinstance(subcorp_idx, int):
                if m['position'][0] != subcorp_idx: continue
            for w in m["left"] + m["right"]:
                o11.update({w: 1})
            C1 += 1
        
        collo_margin = {}
        for w in o11:
            if chinese_only:
                if self.pat_ch_chr.search(w) is None: continue
            if isinstance(subcorp_idx, int):
                collo_margin[w] = len([1 for i in self.index[w] if i[0] == subcorp_idx])
            else:
                collo_margin[w] = len(self.index[w])
        
        output = []
        N = self._get_corp_size(subcorp_idx)
        for w, R1 in collo_margin.items():
            R2 = N - R1
            O11 = o11.get(w, 0)
            O21 = C1 - O11
            O12 = R1 - O11
            O22 = R2 - O21
            O11, O12, O21, O22, E11, E12, E21, E22 = additive_smooth(O11, O12, O21, O22, alpha=alpha)
            stats = { 
                func.__name__: func(O11, O12, O21, O22, E11, E12, E21, E22)\
                    for func in self.association_measures
            }
            stats['RawCount'] = o11.get(w, 0)
            output.append((w, stats))
        
        return sorted(output, reverse=True, key=lambda x: x[1][sort_by])


    corp_size = None
    def _get_corp_size(self, subcorp_idx=None):
        if self.corp_size is None:
            self.corp_size = {}
            for i in range(len(self.corpus)):
                corp = (c for t in self.corpus[i]['text'] for c in t['c'])
                self.corp_size[i] = len(list(chain.from_iterable(corp)))
        if isinstance(subcorp_idx, int):
            return self.corp_size[subcorp_idx]
        return sum(self.corp_size.values())
