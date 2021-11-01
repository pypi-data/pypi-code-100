import json
from pathlib import Path
from .UtilsTextProcess import *


class PlainTextReader:
    """Plain text corpus input handler

    Examples
    --------
    
    .. code-block:: python

        >>> from pprint import pprint
        >>> from gdown import cached_download
        >>> from dcctk.corpusReader import PlainTextReader

        >>> url = 'https://github.com/liao961120/dcctk/raw/main/test/minimal_plaintext_corpus.zip'
        >>> cached_download(url, "minimal_plaintext_corpus.zip", postprocess=gdown.extractall)
        >>> corpus = PlainTextReader("minimal_plaintext_corpus/").corpus
        >>> pprint(corpus)
        
        [{'id': '01',
        'm': {'label': '1st timestep', 'ord': 1, 'time_range': [-1000, -206]},
        'text': [{'c': ['這是第三篇裡的一個句子。', '這是第二個句子。'],
                    'id': '01/text3.txt',
                    'm': {'about': 'Text 3 in 1st timestep'}},
                {'c': ['這是一個句子。', '這是第二個句子。'],
                    'id': '01/text1.txt',
                    'm': {'about': 'Text 1 in 1st timestep'}},
                {'c': ['這是第二篇裡的一個句子。', '這是第二個句子。'],
                    'id': '01/text2.txt',
                    'm': {'about': 'Text 2 in 1st timestep'}}]},
        {'id': '02',
        'm': {'label': '2nd timestep', 'ord': 2, 'time_range': [-205, 220]},
        'text': [{'c': ['這是第三篇裡的一個句子。', '這是第二個句子。'],
                    'id': '02/text3.txt',
                    'm': {'about': 'Text 3 in 2nd timestep'}},
                {'c': ['這是一個句子。', '這是第二個句子。'],
                    'id': '02/text1.txt',
                    'm': {'about': 'Text 1 in 2nd timestep'}},
                {'c': ['這是第二篇裡的一個句子。', '這是第二個句子。'],
                    'id': '02/text2.txt',
                    'm': {'about': 'Text 2 in 2nd timestep'}}]}]
    """

    def __init__(self, dir_path="data/", ts_meta_filename="time.yaml", \
        text_meta_filename="text_meta.yaml", ts_meta_loader=None, 
        text_meta_loader=None, plain_text_reader=read_text_as_sentences, auto_load=True):
        """Read in plain text corpus

        Parameters
        ----------
        dir_path : str, optional
            Path to the directory containing the plain text corpus. For the
            directory structure of the plain text corpus, refer to the example
            data in the GitHub `repo`_. By default "data/".

            .. _repo: https://github.com/liao961120/dcctk/tree/main/test/data
        ts_meta_filename : str, optional
            Path to the metadata file specifying the time info of each 
            timestepped subcorpora, by default "time.yaml".
        text_meta_filename : str, optional
            Path to the metadata file specifying info of each corpus text, 
            by default "text_meta.yaml".
        ts_meta_loader : Callable, optional
            Custom function to parse the file specified in 
            :code:`ts_meta_filename`, by default None.
        text_meta_loader : Callable, optional
            Custom function to parse the file specified in 
            :code:`text_meta_filename`, by default None.
        plain_text_reader : Callable, optional
            Function to read a corpus text file as a sequence of sentences, 
            by default :func:`dcctk.UtilsTextProcess.read_text_as_sentences`.
        """
        # Attributes
        self.corp_path = Path(dir_path)
        self.corpus = []
        self.n_subcorp = len([1 for x in self.corp_path.iterdir() if x.is_dir()])
        self.text_meta = {}
        self.timestep_meta = {}
        self.plain_text_reader = plain_text_reader
        self.timestep_meta = self._get_meta(self.corp_path / ts_meta_filename, custom_loader=ts_meta_loader)
        self.text_meta = self._get_meta(self.corp_path / text_meta_filename, custom_loader=text_meta_loader)
        if auto_load:
            self._read_corpus()


    def get_corpus_as_gen(self):
        for dir_ in sorted(self.corp_path.iterdir()):
            if not dir_.is_dir(): continue
            # Construct corpus
            meta = {}
            for k, v in self.timestep_meta.get(dir_.stem, {}).items():
                meta[k] = v
            yield {
                'id': dir_.stem,
                'm': meta,
                'text': self._get_texts_as_gen(dir_.glob("*.txt"))
            }


    def _get_texts_as_gen(self, fps):
        for fp in fps:
            text_id, text_meta, text_content = self._read_text(fp)
            text = {
                'id': text_id,
                'm': text_meta,
                'c': list(text_content)  # A list of sentences
            }
            yield text

    def _read_corpus(self):
        for dir_ in sorted(self.corp_path.iterdir()):
            if not dir_.is_dir(): continue
            
            # Construct corpus
            meta = {}
            for k, v in self.timestep_meta.get(dir_.stem, {}).items():
                meta[k] = v
            corpus = {
                'id': dir_.stem,
                'm': meta,
                'text': []
            }

            # Read text
            for fp in dir_.glob("*.txt"):
                text_id, text_meta, text_content = self._read_text(fp)
                text = {
                    'id': text_id,
                    'm': text_meta,
                    'c': list(text_content)  # A list of sentences
                }
                corpus["text"].append(text)

            self.corpus.append(corpus)


    def _read_text(self, fp):
        meta = {}
        fp_key = f"{fp.parent.stem}/{fp.name}"
        for k, v in self.text_meta.get(fp_key, {}).items():
            meta[k] = v

        return fp_key, meta, self.plain_text_reader(fp)


    def _get_meta(self, fp, custom_loader=None):
        if not fp.exists(): return {}
        with open(fp, encoding="utf-8") as f:
            if custom_loader:
                return custom_loader()
            elif fp.name.endswith('yaml'):
                import yaml
                return yaml.load(f, Loader=yaml.FullLoader)
            elif fp.name.endswith('json'):
                return json.load(f)
