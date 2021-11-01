# Make some synthetic data from, e.g., Poisson and Negative Binomial
# distributions.

import datetime
import numpy as np


class synthetic_data():
    # Note: "features" = "exogenous  variables"
    #       "labels"   = "endogenous variables"

    def __init__(self,
                 N=100000,
                 num_features=8,
                 true_betas=None,
                 distribution='Poisson',
                 train_fraction=.6,
                 test_fraction=.3,
                 valid_fraction=.1,
                 exposure=False,
                 random_seed=None,
                 ):
        self.random_seed = random_seed
        if random_seed is None:
            self.random_seed = hash(str(datetime.datetime.now()))
        self.rng = np.random.default_rng(random_seed)

        self.N = N
        self.num_features = num_features
        assert distribution in ['Poisson', 'Negative Binomial']
        self.distribution = distribution
        self.fractions = {'train': train_fraction,
                          'test': test_fraction,
                          'valid': valid_fraction}

        self.has_exposure = exposure
        if true_betas is None:
            self.make_betas()
        else:
            self.true_betas = true_betas

        self.make_features()
        self.make_params()
        self.make_exposure()
        self.make_data()
        self.make_train_test_valid_split()

    def make_betas(self):
        self.true_betas = {}
        if self.distribution == 'Poisson':
            b = np.power(self.rng.normal(size=(self.num_features)), 3)
            b /= np.max(np.abs(b))
            self.true_betas['lambda'] = b
        elif self.distribution == 'Negative Binomial':
            self.true_betas['n'] = self.rng.exponential(
                size=self.num_features)
            self.true_betas['p'] = self.rng.uniform(
                size=self.num_features)

    def make_features(self):
        self.features = self.rng.normal(size=(self.N, self.num_features))

    def make_params(self):
        self.params = {}
        if self.distribution == 'Poisson':
            self.params['lambda'] = np.exp(
                self.features @ self.true_betas['lambda'])
        elif self.distribution == 'Negative Binomial':
            # Note: these are non-standard link functions;
            # canonical is "g(mu)=log[mu/ [n*(1+mu/n)]"
            # where mu=np/(1-p)
            self.params['n'] = np.exp(self.features @ self.true_betas['n'])
            # Sigmoid function:
            self.params['p'] = 1 / (
                1 + np.exp(-(self.features @ self.true_betas['p'])))

    def make_exposure(self):
        if self.has_exposure:
            # Exposure is split 50/50 between "a" and "b"
            exposure_a = 1
            exposure_b = 3
            assert exposure_a != exposure_b
            self.exposure = (
                abs(exposure_b-exposure_a) *
                self.rng.integers(2, size=self.N).astype(float))
            self.exposure += min(exposure_a, exposure_b)
            # Useful for debugging...
            # self.exposure = 2 * np.ones(self.N)

    def make_data(self):
        if self.distribution == 'Poisson':
            lam = self.params['lambda']
            if self.has_exposure:
                lam *= self.exposure
            self.labels = self.rng.poisson(
                lam=lam, size=self.N)
        elif self.distribution == 'Negative Binomial':
            n = self.params['n']
            if self.has_exposure:
                n *= self.exposure
            self.labels = self.rng.negative_binomial(
                n=n,
                p=self.params['p'],
                size=self.N)
        if self.has_exposure:
            self.labels = np.vstack([self.labels, self.exposure]).T

    def make_train_test_valid_split(self):
        self.features_split = {}
        self.labels_split = {}
        index = 0
        sum_fractions = 0
        for f in self.fractions:
            count = round(self.fractions[f] * self.N)
            self.features_split[f] = self.features[index: index+count]
            self.labels_split[f] = self.labels[index: index+count]
            index += count
            sum_fractions += self.fractions[f]
        assert index <= self.N
        assert sum_fractions <= 1
