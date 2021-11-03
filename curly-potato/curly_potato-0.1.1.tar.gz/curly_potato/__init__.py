"""
curly_potato

An example python library.
"""

__version__ = "0.1.1"
__author__ = 'Eugene Chernatskiy'
__credits__ = 'ITMO University'

import numpy
from typing import List, Tuple, Union
def fast_hist(array: List[Union[int, float]], 
              bins: int) -> Tuple[List[int], List[float]]:
    minElem, maxElem = min(array), max(array)
    delta = (maxElem - minElem) / bins
    countInBin = numpy.zeros(bins)
    for elem in array:
        countInBin[min(int((elem - minElem) / delta), bins - 1)] += 1
    return (numpy.array([int(x) for x in countInBin]), numpy.arange(minElem, maxElem, delta))

import matplotlib.pyplot
def plot_discrete(array: List[Union[int, float]], bins: int = 10, width: float = 0.8):
    value_counts, bins_names = fast_hist(array, bins)
    matplotlib.pyplot.bar(bins_names + width / 2, value_counts, width = width)