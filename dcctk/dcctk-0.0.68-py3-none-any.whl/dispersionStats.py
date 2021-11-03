from math import log2, sqrt
from statistics import mean, pstdev


def Range(d: dict, t:int=1):
    return sum(1 for v in d['v'] if v >= t)


def DP(d: dict):
    V, S, F, n = d['v'], d['s'], d['f'], d['n']
    if F == 0: return 0
    return 0.5 * sum( abs((V[i] / F) - S[i]) for i in range(n) )


def DPnorm(d: dict):
    s = DP(d)
    if s == 0: return 0
    return s / ( 1 - min(d['s']) )


def KLdivergence(d: dict):
    V, S, F, n = d['v'], d['s'], d['f'], d['n']
    stat = 0
    for i in range(n):
        if V[i] == 0: continue
        a = V[i] / F
        stat += a * log2(a / S[i])
    return stat


def JuillandD(d: dict):
    P, n = d['p'], d['n']
    d = mean(P) * sqrt(n - 1)
    if d == 0: return None
    return 1 - ( pstdev(P) / d )


def RosengrenS(d: dict):
    V, S, F, n = d['v'], d['s'], d['f'], d['n']
    if F == 0: return None
    return sum(sqrt(S[i] * V[i]) for i in range(n)) ** 2 / F
