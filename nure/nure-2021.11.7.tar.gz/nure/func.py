from typing import Callable, Iterable


def chain(*l_func: Iterable[Callable]):
    def __wrapper__(argument):
        for func in l_func:
            argument = func(argument)

        return argument

    return __wrapper__


def from_iterable(func: Callable):
    def __wrapper__(iterable_arguments: Iterable):
        return func(*iterable_arguments)

    return __wrapper__
