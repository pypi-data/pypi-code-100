from abc import ABC, abstractmethod
from typing import TypeVar, Callable, Generic
# from collections.abc import Callable


from grass.function import flip

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

class Functor(ABC, Generic[A]):
    '''函子'''
    @abstractmethod
    def fmap(self, f: Callable[[A], B]) -> Functor[B]:
        pass

def map(f: Callable[[A], B], fa: Functor[A]) -> Functor[B]:
    if isinstance(fa, Functor):
        return fa.fmap(f)
    else:
        raise ValueError


mapFlipped = flip(map)
