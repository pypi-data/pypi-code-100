import numpy as np
import pandas as pd
import toad

from .. import io_helper
from ..model_helper import score_mapping


class ScoreBin:
    @classmethod
    def fit_transform(cls, pdf_train, pdf_test, label, prob, score, low, high, low_rate, high_rate, **kwargs):
        fp_score = kwargs.get('fp_score', None)

        sm = score_mapping.ScoreMapping(n_bins=25, n_degree=1, score_type='customize')
        sm.fit(pdf_train[prob], pdf_train[label],
               mapping={low: low_rate, high: high_rate},
               min_score=low, max_score=high)

        pdf_train[score] = sm.transform(pdf_train[prob])
        pdf_test[score] = sm.transform(pdf_test[prob])

        if fp_score is not None:
            fp_score = str(fp_score)
            io_helper.Dir.get_or_create(fp_score)
            io_helper.Pickle.save(sm, f"{fp_score}")

        return pdf_train, pdf_test

    @classmethod
    def fit_transform_subscore(cls, pdf_train, pdf_test, label, prob, score, **kwargs):
        pdf_train, pdf_test = cls.fit_transform(pdf_train, pdf_test, label, prob, score,
                                                30, 85, 0.128, 0.001, **kwargs)

        return pdf_train, pdf_test

    @classmethod
    def fit_transform_megascore(cls, pdf_train, pdf_test, label, prob, score, **kwargs):
        pdf_train, pdf_test = cls.fit_transform(pdf_train, pdf_test, label, prob, score,
                                                500, 850, 0.128, 0.001, **kwargs)

        return pdf_train, pdf_test

    @classmethod
    def transform(cls, pdf_score, prob, score, fp_score):
        sm = io_helper.Pickle.load(fp_score)
        pdf_score[score] = sm.transform(pdf_score[prob])

        return pdf_score

    @classmethod
    def bin_quantile(cls, pdf_score, label, score, **kwargs):
        n_bins = kwargs.get('n_bins', 10)
        bin_name = kwargs.get('bin_name', 'bin')

        combiner = toad.transform.Combiner()

        combiner.fit(pdf_score[[score, label]], y=label,
                     method='quantile',
                     n_bins=n_bins,
                     empty_separate=True)

        pdf_score[bin_name] = combiner.transform(pdf_score[[score]], labels=True)

        return pdf_score

    @classmethod
    def bin_quantile_sub(cls, pdf_sub, pdf_score, label, score, **kwargs):
        n_bins = kwargs.get('n_bins', 10)
        bin_name = kwargs.get('bin_name', 'bin')

        combiner = toad.transform.Combiner()

        combiner.fit(pdf_sub[[score, label]], y=label,
                     method='quantile',
                     n_bins=n_bins,
                     empty_separate=True)

        pdf_score[bin_name] = combiner.transform(pdf_score[[score]], labels=True)

        return pdf_score

    @classmethod
    def bin_step(cls, pdf_score, label, score, **kwargs):
        n_bins = kwargs.get('n_bins', 10)
        bin_name = kwargs.get('bin_name', 'bin')
        combiner = toad.transform.Combiner()

        combiner.fit(pdf_score[[score, label]], y=label,
                     method='step',
                     n_bins=n_bins,
                     empty_separate=True)

        pdf_score[bin_name] = combiner.transform(pdf_score[[score]], labels=True)

        return pdf_score

    @classmethod
    def bin_given(cls, pdf_score, score, splits, **kwargs):
        bin_name = kwargs.get('bin_name', 'bin')
        combiner = toad.transform.Combiner()

        combiner.update({score: splits})

        pdf_score[bin_name] = combiner.transform(pdf_score[[score]], labels=True)

        return pdf_score

    @classmethod
    def bin_subscore(cls, pdf_score, score, **kwargs):
        splits = [0, 30] + list(np.arange(50, 90, 5)) + [100]
        return cls.bin_given(pdf_score, score, splits, **kwargs)

    @classmethod
    def bin_megascore(cls, pdf_score, score, **kwargs):
        splits = [0, 300] + list(np.arange(500, 900, 50)) + [1000]
        return cls.bin_given(pdf_score, score, splits, **kwargs)
