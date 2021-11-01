#  Copyright (c) 2021. Davi Pereira dos Santos
#  This file is part of the idict project.
#  Please respect the license - more about this in the section (*) below.
#
#  idict is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  idict is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with idict.  If not, see <http://www.gnu.org/licenses/>.
#
#  (*) Removing authorship by any means, e.g. by distribution of derived
#  works or verbatim, obfuscated, compiled or rewritten versions of any
#  part of this work is illegal and unethical regarding the effort and
#  time spent here.
from functools import cached_property
from json import dumps
from operator import rshift as aop
from operator import xor as cop
from random import Random
from typing import Union, Callable

from ldict.core.base import AbstractLazyDict
from ldict.customjson import CustomJSONEncoder
from ldict.parameter.abslet import AbstractLet


class iLet(AbstractLet):
    """
    Set values or sampling intervals for parameterized functions

    >>> from idict import idict, let
    >>> f = lambda x,y, a=[-1,-0.9,-0.8,...,1]: {"z": a*x + y}
    >>> f_a = let(f, a=0)
    >>> f_a
    λ{'a': 0}
    >>> d = idict(x=5,y=7)
     >>> d2 = d >> f_a
    >>> print(d2)
    {
        "z": "→(a x y)",
        "x": 5,
        "y": 7,
        "id": "tsKSa7giKVTZC-s0qQVQy3nO923A59f327Jd.05S",
        "ids": {
            "z": "Cv907SXx1qXi0b7LJar9VGVxFc6A59f327Jd.05S",
            "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
            "y": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8"
        }
    }
    >>> d2.evaluate()
    >>> print(d2)
    {
        "z": 7,
        "x": 5,
        "y": 7,
        "id": "tsKSa7giKVTZC-s0qQVQy3nO923A59f327Jd.05S",
        "ids": {
            "z": "Cv907SXx1qXi0b7LJar9VGVxFc6A59f327Jd.05S",
            "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
            "y": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8"
        }
    }
    >>> from random import Random
    >>> d2 = d >> Random(0) >> let(f, a=[8,9])
    >>> print(d2)
    {
        "z": "→(a x y)",
        "x": 5,
        "y": 7,
        "id": "qMwvsA4Ll3c7CLVlafJo6o3yP5dEhLZPNh9QkVgv",
        "ids": {
            "z": "Fir2J-MamdlPkZz4uBeJs.BhjggEhLZPNh9QkVgv",
            "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
            "y": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8"
        }
    }
    >>> d2.evaluate()
    >>> print(d2)
    {
        "z": 52,
        "x": 5,
        "y": 7,
        "id": "qMwvsA4Ll3c7CLVlafJo6o3yP5dEhLZPNh9QkVgv",
        "ids": {
            "z": "Fir2J-MamdlPkZz4uBeJs.BhjggEhLZPNh9QkVgv",
            "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
            "y": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8"
        }
    }
    >>> let(f, a=5) >> {"x": 5, "y": 7}
    «λ{'a': 5} × {'x': 5, 'y': 7}»
    >>> print(idict({"x": 5, "y": 7}) >> let(f, a=5))
    {
        "z": "→(a x y)",
        "x": 5,
        "y": 7,
        "id": "rrC7MbIwMVR4rAPcSEgs3kSbJnJuCMS1F1k3.VfQ",
        "ids": {
            "z": "XLoMEFGNqF52tTtX9.NMpXoXcyMuCMS1F1k3.VfQ",
            "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
            "y": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8"
        }
    }
    >>> let(f, a=5) >> idict({"x": 5, "y": 7})
    «λ{'a': 5} × {
        "x": 5,
        "y": 7,
        "id": "mP_2d615fd34f97ac906e162c6fc6aedadc4d140",
        "ids": {
            "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
            "y": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8"
        }
    }»
    >>> let(f, a=5) >> ["mycache"]
    «λ{'a': 5} × ^»
    >>> from idict.parameter.ifunctionspace import iFunctionSpace
    >>> let(f, a=5) >> iFunctionSpace()
    «λ{'a': 5}»
    >>> iFunctionSpace() >> let(f, a=5)
    «λ{'a': 5}»
    >>> (lambda x: {"z": x*8}) >> let(f, a=5)
    «λ × λ{'a': 5}»
    >>> d = {"x":3, "y": 8} >> let(f, a=5)
    >>> print(d)
    {
        "z": "→(a x y)",
        "x": 3,
        "y": 8,
        "id": "cKaaEdvxmlKTqsyOsb8eAJMl4aCuCMS1F1k3.VfQ",
        "ids": {
            "z": "7WQXcDiKAKIjnfIwETM9UknKD9CuCMS1F1k3.VfQ",
            "x": "WB_e55a47230d67db81bcc1aecde8f1b950282cd",
            "y": "6q_07bbf68ac6eb0f9e2da3bda1665567bc21bde"
        }
    }
    >>> print(d.z)
    23
    >>> d >>= Random(0) >> let(f, a=[1,2,3]) >> let(f, a=[9,8,7])
    >>> print(d)
    {
        "z": "→(a x y)",
        "x": 3,
        "y": 8,
        "id": "5Q7U4sm-DkzdUwGKY.9IrQRTpFLMIhJOSvWYkxt-",
        "ids": {
            "z": "oOhgGymI3OqJG1As8IODMrsgZELMIhJOSvWYkxt-",
            "x": "WB_e55a47230d67db81bcc1aecde8f1b950282cd",
            "y": "6q_07bbf68ac6eb0f9e2da3bda1665567bc21bde"
        }
    }
    >>> print(d.z)
    32
    """

    def __init__(self, f, **kwargs):
        self.f = f
        self.config = {k: kwargs[k] for k in sorted(kwargs.keys())}
        self.asdict = self.config

    @cached_property
    def bytes(self):
        return dumps(self.config, sort_keys=True, cls=CustomJSONEncoder).encode()

    def __repr__(self):
        return "λ" + str(self.config)

    def __rrshift__(self, left: Union[dict, list, Random, Callable, 'iLet']):
        """
        >>> from idict.parameter.ilet import iLet
        >>> {"x":5} >> iLet(lambda x:{"x": x**2}, x=5)
        {
            "x": "→(x)",
            "id": "LEMLzqy0ijWZcJ8w37f8QE2tj-7QOh11-DoSoW4j",
            "ids": "LEMLzqy0ijWZcJ8w37f8QE2tj-7QOh11-DoSoW4j"
        }
        >>> [1] >> iLet(lambda x:{"x": x**2}, x=5)
        «^ × λ{'x': 5}»
        """
        if isinstance(left, dict) and not isinstance(left, AbstractLazyDict):
            from idict.core.idict_ import Idict
            return Idict(left) >> self
        if isinstance(left, (list, Random, Callable)):
            from idict.parameter.ifunctionspace import iFunctionSpace
            return iFunctionSpace(left, aop, self)
        return NotImplemented  # pragma: no cover

    def __rshift__(self, other: Union[dict, list, Random, Callable, 'iLet', AbstractLazyDict]):
        """
        >>> iLet(lambda x:{"x": x**2}, x=5) >> [1]
        «λ{'x': 5} × ^»
        """

        if isinstance(other, (dict, list, Random, Callable, iLet)):
            from idict.parameter.ifunctionspace import iFunctionSpace
            return iFunctionSpace(self, aop, other)
        return NotImplemented  # pragma: no cover

    def __rxor__(self, left: Union[dict, list, Random, Callable, 'iLet']):
        if isinstance(left, (dict, list, Random, Callable)) and not isinstance(left, AbstractLazyDict):
            from idict.parameter.ifunctionspace import iFunctionSpace
            return iFunctionSpace(left, cop, self)
        return NotImplemented  # pragma: no cover

    def __xor__(self, other: Union[dict, list, Random, Callable, 'iLet', AbstractLazyDict]):
        if isinstance(other, (dict, list, Random, Callable, iLet)):
            from idict.parameter.ifunctionspace import iFunctionSpace
            return iFunctionSpace(self, cop, other)
        return NotImplemented  # pragma: no cover
