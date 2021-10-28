"""
This file is part of Apricopt.

Apricopt is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Apricopt is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Apricopt.  If not, see <http://www.gnu.org/licenses/>.

Copyright (C) 2020-2021 Marco Esposito, Leonardo Picchiami.
"""

import math

import numpy as np


def ackley(x) -> float:
    """
    The Ackley function
    :param x: the input
    :return: a float
    """
    a = 20
    b = 0.2
    c = 2 * math.pi

    d = len(x)
    sum1 = np.square(x).sum()
    sum2 = np.cos(np.dot(c, x)).sum()

    term1 = -a * np.power(math.e, -b * np.sqrt(sum1 / d))
    term2 = -np.power(math.e, sum2 / d)

    return term1 + term2 + a + math.e
