# coding=utf-8
from nltk.probability import *

from mammut.common import google_api
from mammut.common.util import StringEnum

from mammut.models import (
    NGRAM_VIEWER_SMOOTHING,
    LEXICAL_RELEVANCE_INDEX_ESTIMATOR_CONSOLIDATE_STATS,
    LEXICAL_RELEVANCE_INDEX_ESTIMATOR_AUMENTATION,
    LEXICAL_RELEVANCE_INDEX_ESTIMATOR_USAGE_SOURCE,
)
from mammut.models import NGRAM_VIEWER_YEAR_START
from mammut.models import NGRAM_VIEWER_YEAR_END
from mammut.models import NGRAM_VIEWER_CASE_INSENSITIVE


class BaseNGramProbDist(ProbDistI):
    def __init__(self, regional_settings):
        self.regional_settings = regional_settings
        self._current_max = float(0.0)
        self._current_cond_total = float(0.0)

    def freqdist(self):
        raise NotImplementedError()

    def B(self):
        raise NotImplementedError()

    def has_sample(self, sample):
        raise NotImplementedError()

    def prob(self, sample, add=True):
        raise NotImplementedError()

    def cond_prob(self, sample):
        raise NotImplementedError()

    def max(self):
        return self._current_max

    def samples(self):
        raise NotImplementedError()

    def __repr__(self):
        """
        :rtype: str
        :return: A string representation of this ``ProbDist``.
        """
        return "<NGramProbDist based on %d samples>" % self.B()


class MuteNGramProbDist(BaseNGramProbDist):
    def __init__(self, regional_settings):
        BaseNGramProbDist.__init__(self, regional_settings)
        self._samples = set()

    def freqdist(self):
        raise ValueError("A MuteNGramProbDist is a dummy distribution.")

    def B(self):
        return len(self._samples)

    def has_sample(self, sample):
        return sample in self._samples

    def prob(self, sample, add=True):
        if add:
            self._samples.add(sample)
        return -1.0

    def cond_prob(self, sample, add=True):
        if add:
            self._samples.add(sample)
        return -1.0

    def samples(self):
        return self._samples


class GoogleNGramProbDistMode(StringEnum):
    UNORDERED_TRIGRAM = "utrigram"
    UNORDERED_BIGRAM = "ubigram"
    UNIGRAM = "unigram"


class GoogleNGramProbDist(BaseNGramProbDist):
    def __init__(self, regional_settings, mode: GoogleNGramProbDistMode):
        BaseNGramProbDist.__init__(self, regional_settings)
        self.mode = mode
        self._prob_dict = {}

    def freqdist(self):
        raise ValueError("A GoogleNGramProbDist is a online service.")

    def B(self):
        return len(self._prob_dict)

    def has_sample(self, sample):
        return sample in self._prob_dict

    def prob(self, sample, add=True):
        val = 0.0
        if sample not in self._prob_dict:
            if self.mode == GoogleNGramProbDistMode.UNORDERED_TRIGRAM:
                val = google_api.unordered_trigram_frecuency(
                    sample,
                    self.regional_settings,
                    NGRAM_VIEWER_SMOOTHING,
                    NGRAM_VIEWER_YEAR_START,
                    NGRAM_VIEWER_YEAR_END,
                    NGRAM_VIEWER_CASE_INSENSITIVE,
                )
            elif self.mode == GoogleNGramProbDistMode.UNORDERED_BIGRAM:
                val = google_api.unordered_bigram_frecuency(
                    sample,
                    self.regional_settings,
                    NGRAM_VIEWER_SMOOTHING,
                    NGRAM_VIEWER_YEAR_START,
                    NGRAM_VIEWER_YEAR_END,
                    NGRAM_VIEWER_CASE_INSENSITIVE,
                )
            else:
                val = google_api.unigram_frecuency(
                    sample,
                    self.regional_settings,
                    NGRAM_VIEWER_SMOOTHING,
                    NGRAM_VIEWER_YEAR_START,
                    NGRAM_VIEWER_YEAR_END,
                    NGRAM_VIEWER_CASE_INSENSITIVE,
                )
            if add:
                self._prob_dict[sample] = val
                if val > self._current_max:
                    self._current_max = val
                self._current_cond_total = float(self._current_cond_total) + val
        else:
            val = self._prob_dict[sample]
        return val

    def cond_prob(self, sample, add=True):
        res = float(self.prob(sample, add)) / float(self._current_cond_total)
        return res

    def samples(self):
        return self._prob_dict.keys()


class LexicalRelevanceIndexEstimator:
    def __init__(self, regional_settings, token_freqdist: FreqDist):
        self.regional_settings = regional_settings
        self.prob_d_u_c_base_prior = MLEProbDist(token_freqdist)
        if LEXICAL_RELEVANCE_INDEX_ESTIMATOR_USAGE_SOURCE == "GoogleNgram":
            self.prob_u = GoogleNGramProbDist(
                self.regional_settings, GoogleNGramProbDistMode.UNIGRAM
            )
        else:
            self.prob_u = MuteNGramProbDist(self.regional_settings)

    def add_new_sample(self, sample):
        return self.prob_u.prob(sample)

    def consolidate_stats(self):
        if self.prob_d_u_c_base_prior.freqdist().B() != self.prob_u.B():
            for s in self.prob_d_u_c_base_prior.samples():
                if not self.prob_u.has_sample(s):
                    self.add_new_sample(s)

    def get_index(self, sample, add=True):
        if LEXICAL_RELEVANCE_INDEX_ESTIMATOR_CONSOLIDATE_STATS and not add:
            self.consolidate_stats()
        prob_ng_cond_prob = self.prob_u.cond_prob(sample, add)
        prob_d_u_c_base_prior_prob = self.prob_d_u_c_base_prior.prob(sample)
        prob_ng_prob = self.prob_u.prob(sample, add)
        unnormalized_prob = float(prob_ng_cond_prob) * float(prob_d_u_c_base_prior_prob)
        if unnormalized_prob:
            normalized_prob = float(unnormalized_prob) / float(prob_ng_prob)
            aumented_prob = (
                float(LEXICAL_RELEVANCE_INDEX_ESTIMATOR_AUMENTATION) * normalized_prob
            )
            return aumented_prob
        else:
            return 0.0
