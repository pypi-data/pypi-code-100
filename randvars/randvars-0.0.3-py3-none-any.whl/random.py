"""
Author: John Paul Goodman
Course: ISyE 6644
Semester: Fall 2021
Project Group: 40
"""

import numpy as np
from datetime import datetime


class RandomVariates:
    """
    Class method to generate random variates
    """

    def __init__(self):
        self.seed = None
        self.prn = 0
        self.seed0 = 2 ** 23 - 1
        self.m = 16807
        self.m31 = (2 ** 31 - 1)

    @staticmethod
    def nchoosek(n, k):
        """
        n choose k
        :param n:
        :param k:
        :return:
        """
        n_fact = np.math.factorial(n)
        k_fact = np.math.factorial(k)
        nk_fact = np.math.factorial(n - k)
        res = n_fact / (k_fact * nk_fact)
        return res

    @staticmethod
    def reverse(n=0):
        """
        reverses an integer
        :return: reversed integer
        """
        rev = 0
        while n > 0:
            rev = rev * 10 + n % 10
            n = n // 10
        return rev

    @staticmethod
    def squaresrng(ctr, key):
        """
        B. Widynski
        https://arxiv.org/pdf/2004.06278.pdf
        :param ctr: the center
        :param key: the key
        :return: very large random number
        """
        y = x = ctr * key
        z = y + key
        x = x * x + y
        x = (x >> 32) | (x << 32)  # round 1
        x = x * x + z
        x = (x >> 32) | (x << 32)  # round 2
        x = x * x + y
        x = (x >> 32) | (x << 32)  # round 3
        return (x * x + z) >> 32  # round 4

    def randseed(self):
        """
        Get random number from square
        :return: smaller random number
        """
        i = int(datetime.now().timestamp() * 1000000)
        r = self.reverse(int(datetime.now().timestamp() * 1000000))
        self.prn = self.squaresrng(i, r) % 100000000000
        return self.prn

    def taus(self, n=100):
        """
        Basic Tausworthe Random Number Generator
        :param n: number of random binary values to return
        :return:
        """
        rseed = self.randseed()
        bstring = format(rseed, 'b')
        b = [int(x) for x in bstring]
        blen = len(b)
        r = int(np.round(blen * 0.25))
        q = int(np.round(blen * 0.75))
        for _ in range(n):
            bi = b[blen - r] ^ b[blen - q]
            b.append(bi)
            blen = len(b)
        diff = len(b) - n
        return np.array(b[diff:])

    def tausunif(self, n=1):
        m = 100
        x = self.taus(n=n * m)
        x = [str(i) for i in x]
        it = [iter(x)] * m
        obs = np.array([int(''.join(s), 2) / (2 ** m) for s in zip(*it)])
        return np.array(obs)

    def set_seed(self, seed):
        """
        Set the seed
        :param seed: seed value
        """
        self.seed = seed

    def get_seed(self):
        """
        Get the seed
        """
        return self.seed

    def generateseed(self):
        """
        Generate a random seed if seed value is None. This helps with randomly generating values.
        :return: a seed value
        """
        if self.seed is None:
            self.seed0 = self.randseed()
            seed = (self.m + self.seed0) % self.m31
        else:
            seed = ((self.m + self.seed0 + self.seed) % self.m31) ** np.pi
        return seed

    def uniform(self, a=0, b=1, n=1):
        """
        Generate uniform random variates
        :param n: number of uniform RVs to generate
        :param a: starting point of uniform range
        :param b: ending point of uniform range
        :return: a numpy array of uniform RVs
        """
        unifs = [self.generateseed()]  # type: list[int]
        for i in range(1, n + 1):
            xi = (self.m * unifs[i - 1]) % self.m31
            unifs.append(xi)
        # simple list append is faster than numpy.append()
        # numpy.append() is shockingly slow. this is because it does a full copy?
        return np.array([(((x * (b - a)) / self.m31) + a) for x in unifs][1:])

    def norm(self, mu=0, sd=1, n=1):
        """
        Generate Normal Random Variates
        :param mu: mean
        :param sd: standard deviation
        :param n: number of random normals to generate
        :return: a numpy array of random normals
        """
        u1 = self.uniform(n=n)
        if self.seed is not None:
            self.seed += 2 ** 34 - 1  # Hack to make sure U1 and U2 look independent
        u2 = self.uniform(n=n)
        theta = 2 * np.pi * u2
        r = np.sqrt(-2 * np.log(u1))
        x = r * np.cos(theta)
        z = mu + (x * sd)
        return z

    def exponential(self, lam=1, n=1):
        """
        Generate Exponential Random Variates
        :param lam: lamba or rate
        :param n: the number of random variates to generate
        :return: a numpy array of random exponentials
        """
        if lam == 0 or lam == 0.0:
            return np.zeros(n)  # zeros for summation
        u1 = self.uniform(n=n)
        exp = (-1 / lam) * np.log(1 - u1)
        return exp

    def erlang(self, lam=1, k=1, n=1):
        """
        Generate Erlang Random Variates
        :param lam: lambda or rate
        :param k: shape parameter
        :param n: number of random variates
        :return: a numpy array of random erlang
        """
        erl = np.ones(n)  # ones for product
        for _ in range(k):
            erl *= self.uniform(n=n)
        erl = (-1 / lam) * np.log(erl)
        return erl

    def weibull(self, lam=1, beta=1, n=1):
        """
        Generate Weibull Random Variates
        :param lam: lambda aka the scale
        :param beta: beta aka the shape
        :param n: number of random variates to generate
        :return: a numpy array of random weibull variates
        """
        return (1 / lam) * (-1 * np.log((1 - self.uniform(n=n)))) ** (1 / beta)

    def triangular(self, a=0, b=1, c=2, n=1):
        """
        Generate Triangular Random Variates
        :param a: lower limit of the triangle
        :param b: mode or peak of the triangle
        :param c: upper limit of the triangle
        :param n: number of triangle random variates
        :return: a numpy array of random triangle variates
        """
        f_c = (b - a) / (c - a)
        u = self.uniform(n=n)
        x_tris = []
        for ui in u:
            if ui <= f_c:
                xi = a + np.sqrt(ui * ((b - a) * (c - a)))
                x_tris.append(xi)
            else:
                xi = c - np.sqrt((1.0 - ui) * ((c - b) * (c - a)))
                x_tris.append(xi)
        return np.array(x_tris)

    def bernoulli(self, p=0.5, n=1):
        """
        Generate Bernoulli(p) random variates
        :param p: probability of success
        :param n: number of "coin" tosses
        :return: a numpy array of random "coin" tosses
        """
        u = self.uniform(n=n)
        bp = []
        for ui in u:
            if ui <= 1 - p:
                bp.append(0)
            else:
                bp.append(1)
        return np.array(bp)

    def binomial(self, t=1, p=0.5, n=1):
        """
        Draw samples from a binomial distribution
        :param t: number of bernoulli(p) trials
        :param p: probability of success
        :param n: number of binomial variates to generate
        :return: a numpy array of samples from the parameterized binomial distribution, where each sample is equal to
        the number of successes over the n trials.
        :note: this is clearly not as fast as numpy
        """
        bins = []
        while len(bins) < n:
            v = 0
            for _ in range(t):
                bp = self.bernoulli(p=p)
                if p <= bp:
                    v += 1
                else:
                    v += 0
            bins.append(v)
        return np.array(bins)

    def dicetoss(self, sides=6, n=1):
        """
        Simple dice toss of die with x-side count of "sides" (i.e. 6, 10, 20, etc)
        :param sides: number of sides on the die
        :param n: number of dice tosses
        :return: a numpy array of x-sided dice tosses
        """
        u = self.uniform(n=n)
        return np.ceil(sides*u)

    def geometric(self, p=0.5, n=1):
        """
        Generate geometric random variates
        :param p: probability of success
        :param n: number of geometric random variates to generate
        :return: a numpy array of geometric random variates
        """
        u = self.uniform(n=n)
        return np.ceil(np.log(1-u)/np.log(1-p))

    def negbin(self, t=1, p=0.5, n=1):
        """
        Generate negative binomial random variates
        :param t: number of trials
        :param n: number of random variates to generate
        :param p: probability of success
        :return: a numpy array of random negative binomials
        :note: this is painfully slow for large n
        """
        negbins = []
        while len(negbins) < n:
            v = 0
            for _ in range(t):
                v += self.geometric(p=p)[0]
            negbins.append(v)
        return np.array(negbins)

    def chisq(self, df=1, n=1):
        """
        Generate Chi square random variates with df degrees of freedom
        :param df: degrees of freedom
        :param n: number of random variates to produce
        :return: a numpy array of chi square random variates
        """
        chi = np.zeros(n)
        for _ in range(df):
            chi += self.norm(n=n) ** 2
        return chi

    def poisson(self, lam=1, n=1):
        """
        Generate Poisson random variates
        :param lam: lambda or rate
        :param n: number of random poissons to generate
        :return: a numpy array of random poissons
        """
        p = []
        for _ in range(n):
            t = 0  # initialize sum of exponential variables as zero
            n = -1  # initialize counting variable as negative one
            while t < 1:
                e = self.exponential(lam=lam)[0]
                t += e
                n += 1
            p.append(n)
        return np.array(p)

    def gamma(self, k=1.0, theta=1, n=1):
        """
        Instead of implementing the acceptance-rejection algorithms for generating gamma variates described by
        Law (2015), this is an implementation of Marsaglia and Tsang's transformation-rejection method of using one
        normal variate and one uniform variate as demonstrated in their 2000 paper:
        https://dl.acm.org/doi/10.1145/358407.358414
        :param k: shape parameter
        :param theta: scale parameter
        :param n: number of random gammas to generate
        :return: a numpy array of gamma random variates
        """
        assert k >= 1.0, "k should be at least 1.0"
        assert theta >= 1.0, "theta should be at least 1.0"
        d = k - 1 / 3
        c = 1 / np.sqrt(9 * d)
        gammas = []
        # for _ in range(n):
        while len(gammas) <= n:
            x = self.norm()[0]
            u = self.uniform()[0]
            v = (1 + c * x) ** 3
            if (x > -1 / c) and (np.log(u) < (0.5 * (x ** 2) + d - d * v + d * np.log(v))):
                gammas.append(d * v)
        return theta * np.array(gammas)

    def lognormal(self, mu=0, sd=1, n=1):
        """
        Lognormal Random Variates. The lognormal distribution occasionally referred to as the
        Galton distribution or Galton's distribution, after Francis Galton.
        :param mu: mean
        :param sd: standard deviation
        :param n: number of lognormals to generate
        :return: a numpy array of lognormal random variates
        """
        # 1) Generate Y ~ Nor(u, var)
        # 2) Return X = np.e**Y
        y = self.norm(mu=mu, sd=sd, n=n)
        return np.e**y

    def beta(self, a=1, b=1, n=1):
        """
        Generate beta random variates
        :param a: shape parameter a
        :param b: shape parameter b
        :param n: number of beta random variates to generate
        :return: a numpy array of beta random variates
        """
        # 1) Generate Y1 ~ gamma(a, 1) and Y2 ~ gamma(a, 1)
        # 2) Return X = Y1/(Y1+Y2)
        assert a >= 1.0, "a should be at least 1.0"
        assert b >= 1.0, "b should be at least 1.0"
        y1 = self.gamma(k=a, theta=1, n=n)
        y2 = self.gamma(k=b, theta=1, n=n)
        x = y1 / (y1 + y2)
        return np.array(x)
