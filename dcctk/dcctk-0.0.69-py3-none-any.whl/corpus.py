import re
import json
from itertools import chain
from pathlib import Path
from collections import Counter
from shutil import copyfile
from tqdm.auto import tqdm, trange
from .utils import ngrams
from .UtilsStats import MI, Xsq, Gsq, Dice, DeltaP12, DeltaP21, FisherExact, additive_smooth
from . import database as dbm


class NgramCorpus:
    """Serialized corpus object for computing ngrams from large corpora
    """
    
    association_measures = [
        MI, Xsq, Gsq, Dice, DeltaP21, DeltaP12, FisherExact
    ]

    def __init__(self, corpus_reader, db_dir='dcctk.db/'):
        self.corpus_reader = corpus_reader
        self.n_subcorp = corpus_reader.n_subcorp
        self.database = {}
        self.pat_ch_chr = re.compile("[〇一-\u9fff㐀-\u4dbf豈-\ufaff]")
        self.db_dir = db_dir
        if isinstance(db_dir, str):
            self.db_dir = Path(db_dir)
        if not self.db_dir.exists(): self.db_dir.mkdir()
        self.chr_fq = {
            # 'chr': [100, 50, 250, 300],
            # 'cha': [100, 50, 250, 30]
        }


    @property
    def corpus(self):
        """Return a corpus as a generator
        """
        return self.corpus_reader.get_corpus_as_gen()


    def bigram_associations(self, subcorp_idx=None, chinese_only=True, 
        sort_by="Gsq", reverse=True, fq_thresh=0):
        return sorted(
            list(self.bigram_associations_gen(subcorp_idx, chinese_only, fq_thresh)), reverse=reverse, key=lambda x: x[1][sort_by]
        )


    def bigram_associations_gen(self, subcorp_idx=None, chinese_only=True,fq_thresh=0):
        N = self.get_corpus_size(subcorp_idx)
        for w1w2, o11 in self.freq_distr_ngrams(2, subcorp_idx, chinese_only):
            if o11 < fq_thresh: continue
            w1, w2 = w1w2[0], w1w2[1]
            r1 = self.get_marginal_fq(w1, subcorp_idx)
            r2 = N - r1
            c1 = self.get_marginal_fq(w2, subcorp_idx)
            o12 = r1 - o11
            o21 = c1 - o11
            o22 = r2 - o21
            o11_raw = o11
            o11, o12, o21, o22, e11, e12, e21, e22 = \
                additive_smooth(o11_raw, o12, o21, o22, alpha=0)
            stats = { 
                func.__name__: func(o11, o12, o21, o22, e11, e12, e21, e22)\
                    for func in self.association_measures
            }
            stats['RawCount'] = o11_raw
            yield (w1w2, stats)


    def freq_distr_ngrams(self, n, subcorp_idx=None, chinese_only=True):
        for k, v in self.get_ngrams(n, subcorp_idx).items():
            if chinese_only: 
                if any(not self.pat_ch_chr.search(ch) for ch in k): continue
            yield (k, v)

    
    def get_ngrams(self, n, subcorp_idx=None):
        if isinstance(subcorp_idx, int):
            fn = f'{n}-grams_sc{subcorp_idx}.db'
        else:
            fn = f'{n}-grams_all.db'
        if fn in self.database: 
            return self.database[fn]
        fp = self.db_dir / fn
        if not fp.exists(): self._count_ngrams(n)
        return self.database[fn]


    def get_corpus_size(self, subcorp_idx=None):
        if len(self.chr_fq) == 0: self._count_chr_fq()
        if isinstance(subcorp_idx, int):
            return sum(ss[subcorp_idx] for ss in self.chr_fq.values())
        return sum(chain.from_iterable(self.chr_fq.values()))


    def get_marginal_fq(self, char, subcorp_idx=None):
        if len(self.chr_fq) == 0: self._count_chr_fq()
        fq_lst = self.chr_fq.get(char, [0]*self.n_subcorp)
        if isinstance(subcorp_idx, int):
            return fq_lst[subcorp_idx]
        return sum(fq_lst)


    def load(self, chr_fq:str=None):
        if chr_fq is not None:
            with open(chr_fq, encoding="utf-8") as f:
                self.chr_fq = json.load(f)
        else:
            print("[INFO] Counting char freq...")
            self._count_chr_fq()
        print("[INFO] Connecting to Databases...")
        self._load_db()


    def _load_db(self):
        for db in self.database: self.database[db].close()
        for fn in set(x.name for x in self.db_dir.glob("*.db")):
            fp = str(self.db_dir / fn)
            self.database[fn] = dbm.open(fp, flag="r")
        if len(self.database) == 0:
            print("[WARNING] No db found. Run self._count_ngrams() to calculate ngram data.")


    def _count_chr_fq(self):
        for i, sc in enumerate(self.corpus):
            c = Counter(
                chain.from_iterable(s for t in sc['text'] for s in t['c'])
            )
            for chr, fq in c.items():
                self.chr_fq.setdefault(chr, [0]*self.n_subcorp)[i] += fq
    

    def _count_ngrams(self, n):
        print(f'Counting {n}-grams...')
        if n == 2: self.subcorp_sizes = []
        pbar = tqdm(total=self.n_subcorp)
        ngram = ('', '')
        for i, sc in enumerate(self.corpus):
            subcorp_size = 0
            subcorp_size_zh = 0
            fp = self.db_dir / f'{n}-grams_sc{i}.db'
            db = dbm.open(str(fp), flag='n')
            for text in sc['text']:
                db_tmp = Counter()
                for sent in text['c']:
                    for ngram in ngrams(sent, n=n):
                        # Count coocurrence
                        ng = ''.join(ngram)
                        db_tmp.update({ng: 1})
                        if n == 2:
                            # Count marginal
                            ch = ngram[0]
                            self.chr_fq.setdefault(ch, [0]*self.n_subcorp)[i] += 1 
                            subcorp_size += 1
                            if self.pat_ch_chr.search(ch):
                                subcorp_size_zh += 1
                    if n == 2:
                        # Count last character in sentence
                        ch = ngram[1]
                        if ch != '':
                            self.chr_fq.setdefault(ch, [0]*self.n_subcorp)[i] += 1 
                            subcorp_size += 1
                            if self.pat_ch_chr.search(ch):
                                subcorp_size_zh += 1
                
                # Memory to disk
                for k, v in db_tmp.items():
                    if k not in db:
                        db[k] = v
                        if i != 0: db_all[k] = v
                    else:
                        db[k] = db[k] + v
                        if i != 0: db_all[k] = db_all[k] + v
            db.commit()
            db.close()
            if n == 2:
                self.subcorp_sizes.append( (subcorp_size, subcorp_size_zh) )
            pbar.update(1)

            # Copy first subcorp
            if i == 0:
                fp_all = self.db_dir / f'{n}-grams_all.db'
                if fp_all.exists(): fp_all.unlink()
                copyfile(fp, fp_all)
                db_all = dbm.open(str(fp_all), flag='c')

        db_all.commit()        
        db_all.close()
        pbar.close()
        self._load_db()




class TextBasedCorpus:
    """Corpus object for text-based (text as unit) analysis
    """

    def __init__(self, corpus):
        self.corpus = corpus
        self.pat_ch_chr = re.compile("[〇一-\u9fff㐀-\u4dbf豈-\ufaff]")
        self.path_index = {}
        self.index_path()

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

