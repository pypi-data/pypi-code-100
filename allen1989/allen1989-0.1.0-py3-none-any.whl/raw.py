"""
Raw formalisms as written in paper
"""
import math

von_karman = 0.41  # [-] https://en.wikipedia.org/wiki/Von_K%C3%A1rm%C3%A1n_constant
r1_alfalfa = 100  # [s.m-1] average minimum daytime value of stomatal resistance for a single leaf


def eq3(zm, zh, d, zom, zoh, uz):
    return math.log((zm - d) / zom) * math.log((zh - d) / zoh) / (von_karman ** 2 * uz)


def eq4(hc):
    return 0.123 * hc


def eq5(hc):
    return 0.0123 * hc


def eq6(hc):
    return 0.67 * hc


def eq7(r1, lai):
    return r1 / (0.5 * lai)


def eq8(hc):
    return 24 * hc


def eq9(hc):
    assert hc > 0.03
    return 5.5 + 1.5 * math.log(hc)
