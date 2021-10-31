#%%
from itertools import chain
from collections import Counter
from CompoTree import ComponentTree, Radicals, IDC
from CompoTree import CTFounds

ctree = ComponentTree.load()
radicals = Radicals.load()
idc_names = { x.name for x in IDC }

class CompoAnalysis:

    def __init__(self, IndexedCorpus):
        """[summary]

        Parameters
        ----------
        IndexedCorpus : IndexedCorpus
            A corpus with an index of character positions. Accepts 
            :class:`dcctk.corpus.IndexedCorpus` or its super classes as inputs.
        """
        self.corpus = IndexedCorpus.corpus
        self.index = IndexedCorpus.index
        self.cc_map = {}
        self.rad_map = {}
        self.idc_map = {}
        self.fq_distr_cache = {}
        self.corp_fq_info = {}
        self._build_cc_map()
        self._build_rad_map()
        self._build_idc_map()


    def productivity(self, radical=None, compo=None, idc=None, pos=-1, 
                     subcorp_idx:int=None, text_idx:int=None):

        chr_fq = self.freq_distr(subcorp_idx, text_idx, "chr")
        if radical:
            chars = self.rad_map.get(radical, set())
        elif compo:
            chars = self._component_search(compo, idc, pos)
        elif idc:
            chars = self._idc_search(idc)
        else:
            raise Exception("One of `radical`, `compo`, or `idc` must be given")
        chars.intersection_update(chr_fq.keys())

        V1C, NC = 0, 0
        for ch in chars:
            fq = chr_fq[ch]
            NC += fq
            if fq == 1: V1C += 1
        
        # Static info
        k = (subcorp_idx, text_idx)
        if k not in self.corp_fq_info:
            self.corp_fq_info[k] = {
                'N': sum(chr_fq.values()),
                'V1': sum(f for f in chr_fq.values() if f == 1)
            }

        V1 = self.corp_fq_info[k]['V1']
        return {
            'productivity': {
                'realized': len(chars),
                'expanding': V1C / V1,
                'potential': V1C / NC if V1C != 0 else 0,
            },
            'N': self.corp_fq_info[k]['N'],
            'V1': V1,
            'V1C': V1C,
            'NC': NC
        }

    def _component_search(self, compo:str, idc=None, pos:int=-1):
        bottom_hits = ctree.find(compo, max_depth=1, bmp_only=True)
        if idc is None:
            return set( x[0] for x in CTFounds(bottom_hits)\
                .tolist() )
        return set( x[0] for x in CTFounds(bottom_hits)\
            .filter(idc=IDC[idc].value, pos=pos)\
            .tolist() )

    
    def _idc_search(self, idc:str="vert2"):
        global idc_names
        if idc not in idc_names: 
            raise Exception(f"Invalid IDC value `{idc}`!", 
                            f"IDC must be one of {', '.join(idc_names)}")
        return self.idc_map.get(idc, set())



    def freq_distr(self, subcorp_idx=None, text_idx=None, tp="idc", 
                   compo=None, idc=None, pos=-1, radical=None):
        """Frequency distribution of character (component)

        Parameters
        ----------
        subcorp_idx : int, optional
            Index for subcorpus, by default None, which uses the whole corpus.
        text_idx : int, optional
            Index for text in a subcorpus, by default None, which uses the 
            whole subcorpus.
        tp : str, optional
            One of :code:`chr` (Character), :code:`idc` 
            (Ideographic Description Characters), :code:`rad` (Radical), 
            and None, by default :code:`idc`

        Returns
        -------
        Counter
            A freqeuncy distribution.
        """
        # Use cache
        k = (subcorp_idx, text_idx, tp, compo, idc, pos, radical)
        if k in self.fq_distr_cache: return self.fq_distr_cache[k]

        # Character frequency distribution
        if tp == 'chr' or tp == 'char':
            self.fq_distr_cache[k] = self._freq_distr_chr(subcorp_idx, text_idx)
            return self.fq_distr_cache[k]
        
        # Character component frequency distribution
        fq_ch = self._freq_distr_chr(subcorp_idx, text_idx)
        if tp == "idc" or tp == "rad":
            fq_compo = Counter()
            for ch, fq in fq_ch.items():
                k = "noChrData"
                if ch in self.cc_map:
                    k = self.cc_map[ch].get(tp, "noCompoData")
                fq_compo.update({k: fq})
            self.fq_distr_cache[k] = fq_compo
            return fq_compo
        
        # Token distribution within a radical/component
        if radical:
            chars = self.rad_map.get(radical, set())
            chars.intersection_update(fq_ch.keys())
            return Counter({ch:fq for ch, fq in fq_ch.items() if ch in chars})
        if compo:
            chars = self._component_search(compo, idc, pos)
            chars.intersection_update(fq_ch.keys())
            return Counter({ch:fq for ch, fq in fq_ch.items() if ch in chars})


    def _freq_distr_chr(self, subcorp_idx:int=None, text_idx:int=None):
        if isinstance(text_idx, int) and isinstance(subcorp_idx, int):
            corp = self.corpus[subcorp_idx]['text'][text_idx]['c']
            return Counter(chain.from_iterable(corp))
        if isinstance(subcorp_idx, int):
            corp = (c for t in self.corpus[subcorp_idx]['text'] for c in t['c'])
            return Counter(chain.from_iterable(corp))
        
        corp = (c for sc in self.corpus for t in sc['text'] for c in t['c'])
        return Counter(chain.from_iterable(corp))


    def _build_cc_map(self):
        for ch in self.index:
            idc = ctree.ids_map.get(ch, [None])[0]
            rad = radicals.query(ch)[0]
            dph = None
            if idc is not None:
                idc = idc.idc
                dph = ctree.query(ch, use_flag="shortest", max_depth=-1)[0]
                if not isinstance(dph, str):
                    dph = dph.depth()
                else:
                    dph = 0
            if idc is None and rad == '': continue
            self.cc_map[ch] = {
                'idc': idc,
                'rad': rad,
                'dph': dph
            }
    
    def _build_rad_map(self):
        for ch in self.cc_map:
            r = self.cc_map[ch]['rad']
            self.rad_map.setdefault(r, set()).add(ch)

    def _build_idc_map(self):
        idc_val_nm = { x.value: x.name for x in IDC }
        for ch in self.index.keys():
            idc = ctree.ids_map.get(ch, [None])[0]
            if idc is None: continue
            idc = idc_val_nm.get(idc.idc)
            if idc:
                self.idc_map.setdefault(idc, set()).add(ch)
