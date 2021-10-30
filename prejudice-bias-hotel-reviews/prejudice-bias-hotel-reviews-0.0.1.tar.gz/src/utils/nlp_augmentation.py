import nltk
import fasttext
import string
import math
import spacy
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

from random import sample
from somajo import SoMaJo
from transformers import MarianMTModel, MarianTokenizer
from typing import Union

from src.dataset.utils import load_ethnicities
from src.preprocessing.preprocessor import Preprocessor


class NLPAugmenter:
    def __init__(self,
                 ft_model: Union[fasttext.FastText._FastText, None],
                 ethnicities_file: str = 'ethnien.txt',
                 target_model_name: str = 'Helsinki-NLP/opus-mt-de-en',
                 origin_model_name: str = 'Helsinki-NLP/opus-mt-en-de',):

        # load the models for back-translation
        self.target_tokenizer = MarianTokenizer.from_pretrained(target_model_name)
        self.target_model = MarianMTModel.from_pretrained(target_model_name)

        self.origin_tokenizer = MarianTokenizer.from_pretrained(origin_model_name)
        self.origin_model = MarianMTModel.from_pretrained(origin_model_name)

        # tokenizer specialized to German social media data
        self.tokenizer = SoMaJo("de_CMC", split_camel_case=True)

        # download utils
        nltk.download('punkt', quiet=True)

        # tagging model
        self.spacy_model = spacy.load("de_core_news_sm")

        # FastText model
        fasttext.FastText.eprint = lambda x: None
        if ft_model is not None:
            self.ft_model = ft_model
        else:
            fasttext.util.download_model('de', if_exists='ignore')
            self.ft_model = fasttext.load_model('cc.de.300.bin')

        # load ethnicities from file
        self.ethnien = load_ethnicities(ethnicities_file,
                                        self.ft_model,
                                        add_adj=False,
                                        add_neigh=False,
                                        remove_umlaut=False)
        self.ethnien_rep = self._load_ethnicity_replacements(
            ethnicities_file)

    @staticmethod
    def translate(texts, model, tokenizer, language="en"):
        # transform text into appropriate format for the model
        src_texts = [f">>{language}<< {text}" for text in texts]

        # tokenize the texts
        encoded = tokenizer.prepare_seq2seq_batch(src_texts,
                                                  return_tensors='pt')

        # Generate translation using model
        translated = model.generate(**encoded)

        # Convert the generated tokens indices back into text
        translated_texts = tokenizer.batch_decode(translated,
                                                  skip_special_tokens=True)

        return translated_texts

    def back_translate(self, texts, source_lang="de", target_lang="en"):
        # translate to target language
        target_lang_texts = NLPAugmenter.translate(texts,
                                                   self.target_model,
                                                   self.target_tokenizer,
                                                   language=target_lang)

        # translate from target language back to source language
        back_translated_texts = NLPAugmenter.translate(target_lang_texts,
                                                       self.origin_model,
                                                       self.origin_tokenizer,
                                                       language=source_lang)

        return back_translated_texts

    def _load_ethnicity_replacements(self, ethnicities_file):
        df_ethnien = load_ethnicities(ethnicities_file,
                                      self.ft_model,
                                      return_df=True)
        extension = [
            item.strip() for sublist in df_ethnien['Adjektiv']
            for item in sublist
        ]
        extension1 = [Preprocessor.pluralize(x) + ' Frauen' for x in extension]
        extension2 = [Preprocessor.pluralize(x) + ' Männer' for x in extension]
        extension3 = [Preprocessor.pluralize(x) + ' Gäste' for x in extension]
        extension = extension1 + extension2 + extension3
        extension.append('Frauen')
        extension.append('Männer')
        extension.append('Gäste')
        extension = list(set([x.strip() for x in extension]))

        plur_natio = [
            item.strip() for sublist in df_ethnien['Einwohner']
            for item in sublist
        ]
        plur_natio = set([Preprocessor.pluralize(word) for word in plur_natio])
        plur_natio.discard('')
        plur_natio = list(plur_natio)

        ethnien_choice = plur_natio + extension

        return ethnien_choice

    def _get_neighbors(self, word: str, k: int = 20):
        return self.ft_model.get_nearest_neighbors(word, k=k)

    def _random_replacement_synonym(self,
                                    sent_tokens,
                                    sent_token_ids,
                                    rnd_synonym):
        # calculate how many tokens should be randomly replaced
        n_word_replace = math.ceil((len(sent_tokens) / 100) * rnd_synonym)

        # make sure that the n.o. words to replace isn't greater than max len
        if n_word_replace > len(sent_token_ids):
            n_word_replace = len(sent_token_ids)

        # randomly sample which tokens to replace
        ids_replace = sample(sent_token_ids, k=n_word_replace)
        words_replace = [sent_tokens[x] for x in ids_replace]

        # random sample the replacement of the tokens using FastText embedding
        syn_replace = [
            sample([x[1] for x in self._get_neighbors(word, k=20)], k=1)[0]
            for word in words_replace
        ]

        # loop over tokens and replace
        for rep_w, ind_w in tuple(zip(syn_replace, ids_replace)):
            sent_tokens[ind_w] = rep_w

        return sent_tokens

    def _random_replacement_nationality(self, sent_tokens):
        natio_sent = list(set(sent_tokens) & set(self.ethnien))
        natio_sent = [(sample(self.ethnien_rep, k=1)[0], sent_tokens.index(x))
                      for x in natio_sent]

        # loop over tokens and replace nations
        for rep_w, ind_w in natio_sent:
            sent_tokens[ind_w] = rep_w

        return sent_tokens

    def augment_sample(self, sentence, rnd_synonym=70):
        # tokenize sentence and create token id list
        sent_tokens = [[token.text for token in sent]
                       for sent in self.tokenizer.tokenize_text([sentence])]
        sent_tokens = sent_tokens[0]
        sent_token_ids = list(range(len(sent_tokens)))

        # filter out the tokens that shouldn't be replaced
        sent_token_ids = [
            x for x in sent_token_ids
            if sent_tokens[x] not in set(self.ethnien)
            and not [t.tag_ for t in self.spacy_model(sent_tokens[x])][0] in ['ART']
            and not sent_tokens[x] in string.punctuation
        ]

        # random replace synonym
        sent_tokens = self._random_replacement_synonym(
            sent_tokens=sent_tokens,
            sent_token_ids=sent_token_ids,
            rnd_synonym=rnd_synonym)

        # replace nationalities
        sent_tokens = self._random_replacement_nationality(
            sent_tokens=sent_tokens)

        # back-translation
        sent = ' '.join(sent_tokens)
        sent = self.back_translate([sent])[0]

        return sent
