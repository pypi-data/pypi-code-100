import re
from collections import Counter
from tqdm.auto import trange
from .utils import ngrams
from .UtilsStats import MI, Xsq, Gsq, Dice, DeltaP12, DeltaP21, additive_smooth

class TextBasedCorpus:
    """Corpus object for text-based (text as unit) analysis
    """
    
    association_measures = [
        MI, Xsq, Gsq, Dice, DeltaP21, DeltaP12
    ]

    def __init__(self, corpus):
        self.corpus = corpus
        self.path_index = {}
        self.index_path()
        self.pat_ch_chr = re.compile("[〇一-\u9fff㐀-\u4dbf豈-\ufaff]")

    def bigram_associations(self, subcorp_idx=None, chinese_only=True, sort_by="Gsq", alpha=0):
        distr = self.freq_distr_ngrams(2, subcorp_idx, chinese_only)
        N = sum(distr.values())
        R1 = Counter()
        C1 = Counter()
        for w1w2, fq in distr.items():
            w1, w2 = w1w2[0], w1w2[1]
            R1.update({w1: fq})
            C1.update({w2: fq})
        
        output = []
        for w1w2, o11 in distr.items():
            w1, w2 = w1w2[0], w1w2[1]
            r1 = R1.get(w1, 0)
            r2 = N - r1
            c1 = C1.get(w2, 0)
            o12 = r1 - o11
            o21 = c1 - o11
            o22 = r2 - o21
            o11_raw = o11
            o11, o12, o21, o22, e11, e12, e21, e22 = \
                additive_smooth(o11_raw, o12, o21, o22, alpha)
            stats = { 
                func.__name__: func(o11, o12, o21, o22, e11, e12, e21, e22)\
                    for func in self.association_measures
            }
            stats['RawCount'] = o11_raw
            output.append((w1w2, stats))

        return sorted(output, reverse=True, key=lambda x: x[1][sort_by])


    def freq_distr_ngrams(self, n, subcorp_idx=None, chinese_only=True):
        if (not hasattr(self, 'ngrams')) or (n not in self.ngrams):
            self._count_ngrams(n)
        
        if isinstance(subcorp_idx, int):
            distr =  self.ngrams[n].get(subcorp_idx, Counter())
        else:
            for i, key in enumerate(self.ngrams[n]):
                if i == 0: distr = self.ngrams[n][key].copy()
                else: distr.update(self.ngrams[n][key])
        
        if chinese_only: 
            for k in list(distr.keys()):
                if sum(1 for ch in k if self.pat_ch_chr.search(ch)) < n:
                    del distr[k]
        
        return distr


    def _count_ngrams(self, n):
        print(f'Counting {n}-grams...')
        if not hasattr(self, 'ngrams'): self.ngrams = {}
        self.ngrams[n] = {}
        for i in trange(len(self.corpus)):
            self.ngrams[n][i] = Counter()
            for text in self.corpus[i]['text']:
                for sent in text['c']:
                    for ngram in ngrams(sent, n=n):
                        ng = ''.join(ngram)
                        self.ngrams[n][i].update({ng: 1})


    def get_texts(self, pattern, texts_as_str=False, sents_as_str=True):
        texts = {}
        for id in self._list_pattern(pattern):
            text = self.get_text(id, as_str=False)
            if text is None: continue
            if sents_as_str:
                texts[id] = '\n'.join(text)
            else:
                texts[id] = text
        if texts_as_str: 
            return '\n'.join(texts.values())
        return texts
            

    def get_text(self, id, as_str=False):
        idx = self.path_index.get(id, None)
        if idx is None or isinstance(idx, int): 
            return None
        i, j = idx
        text = self.corpus[i]['text'][j].get('c', [])
        if as_str:
            text = '\n'.join(text)
        return text


    def get_meta_by_path(self, id):
        idx = self.path_index.get(id, None)
        if idx is None:
            return {}
        if isinstance(idx, int):
            return self.corpus[idx].get('m', {})
        if isinstance(idx, tuple):
            i, j = idx
            return self.corpus[i]['text'][j].get('m', {})
        return {}


    def list_files(self, pattern, generator=False):
        if generator:
            return self._list_pattern(pattern)
        return list(self._list_pattern(pattern))


    def _list_pattern(self, pattern):
        pattern = re.compile(pattern)
        for k in self.path_index.keys():
            if pattern.search(k):
                yield k


    def index_path(self):
        print("Indexing corpus for text retrival...")
        for i in trange(len(self.corpus)):
            self.path_index[self.corpus[i]['id']] = i
            for j, text in enumerate(self.corpus[i]['text']):
                self.path_index[text['id']] = (i, j)



class IndexedCorpus(TextBasedCorpus):
    """Corpus object for fast concordance search
    """

    def __init__(self, corpus) -> None:
        TextBasedCorpus.__init__(self, corpus)
        self.index = {}
        self.index_corpus()
    

    def get_meta(self, subcorp_idx, text_idx=None, keys:list=None, include_id=True):
        if text_idx is None:
            meta = self.corpus[subcorp_idx]['m']
            if include_id:
                meta['id'] = self.corpus[subcorp_idx]['id']
        else:
            meta = self.corpus[subcorp_idx]['text'][text_idx]['m']
            if include_id:
                meta['id'] = self.corpus[subcorp_idx]['text'][text_idx]['id']
        if keys:
            keys.append('id')
            return { k:meta[k] for k in keys if k in meta }
        return meta


    def index_corpus(self):
        print("Indexing corpus for concordance search...")
        for i in trange(len(self.corpus)):
            for j, text in enumerate(self.corpus[i]['text']):
                for k, sent in enumerate(text['c']):
                    for l, char in enumerate(sent):
                        if char not in self.index:
                            self.index[char] = []
                        self.index[char].append( (i, j, k, l) )

