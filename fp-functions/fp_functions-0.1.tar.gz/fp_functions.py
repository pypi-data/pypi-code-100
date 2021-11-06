from typing import Iterable, Any
import builtins
import itertools
import more_itertools


class Function:
    _function: "function"

    def __init__(self, function: "function") -> None:
        self._function = function

    def __ror__(self: "Function", left: Iterable) -> Iterable:
        return self._function.__call__(left)

    def __rshift__(self, right: "Function") -> "Function":
        return Function(lambda *args, **kwargs: right._function.__call__(self._function.__call__(*args, **kwargs)))

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self._function(*args, **kwargs)


class Pipe:
    _function: "function"

    def __init__(self, function: "function"):
        self._function = function

    def __call__(self, *args: list, **kwargs: dict) -> Function:
        return Function(lambda x: self._function.__call__(x, *args, **kwargs))


@Pipe
def select(iterable: Iterable, function: "function") -> Iterable:
    return (function.__call__(i) for i in iterable)


@Pipe
def where(iterable: Iterable, function: "function") -> Iterable:
    return (i for i in iterable if function.__call__(i))


@Pipe
def max(iterable: Iterable, **kwargs) -> Iterable:
    return builtins.max(iterable, **kwargs)


@Pipe
def min(iterable: Iterable, **kwargs) -> Iterable:
    return builtins.min(iterable, **kwargs)


@Pipe
def count(iterable: Iterable) -> float:
    return len(iterable)


@Pipe
def take(iterable: Iterable, amount: int) -> Iterable:
    return more_itertools.take(iterable, amount)


@Pipe
def skip(iterable: Iterable, amount: int) -> Iterable:
    for i in iterable:
        if amount == 0:
            yield i
        else:
            amount -= 1


@Pipe
def tail(iterable: Iterable, amount: int) -> Iterable:
    return more_itertools.tail(amount, iterable)


@Pipe
def first(iterable: Iterable) -> Any:
    return more_itertools.first(iterable)


@Pipe
def last(iterable: Iterable) -> Any:
    return more_itertools.last(iterable)


@Pipe
def all(iterable: Iterable, predicate: "function") -> bool:
    return builtins.all(map(predicate, iterable))


@Pipe
def any(iterable: Iterable, predicate: "function") -> bool:
    return builtins.any(map(predicate, iterable))


@Pipe
def chunked(iterable: Iterable, n: int, strict: bool = False) -> list[list[Any]]:
    return more_itertools.chunked(iterable, n, strict)


@Pipe
def permutations(iterable: Iterable, r: int | None = None) -> Iterable:
    for i in itertools.permutations(iterable, r):
        yield i


@Pipe
def distinct_permutations(iterable: Iterable, r: int | None = None) -> Iterable:
    return more_itertools.distinct_permutations(iterable, r)


@Pipe
def combinations(iterable: Iterable, r: int) -> Iterable:
    return itertools.combinations(iterable, r)


@Pipe
def combinations_with_replacement(iterable: Iterable, r: int) -> Iterable:
    return itertools.combinations_with_replacement(iterable, r)


@Pipe
def distinct_combinations(iterable: Iterable, r: int) -> Iterable:
    return more_itertools.distinct_combinations(iterable, r)


@Pipe
def circular_shifts(iterable: Iterable) -> Iterable:
    return more_itertools.circular_shifts(iterable)


@Pipe
def partitions(iterable: Iterable) -> Iterable:
    return more_itertools.partitions(iterable)


@Pipe
def set_partitions(iterable: Iterable, k: int | None = None) -> Iterable:
    return more_itertools.set_partitions(iterable, k)


@Pipe
def partition(iterable: Iterable, predicate: "function") -> Iterable:
    return more_itertools.partition(predicate, iterable)


@Pipe
def random_product(iterable: Iterable, repeat: int = 1, *args) -> tuple:
    return more_itertools.random_product(iterable, repeat=repeat, *args)


@Pipe
def random_permutation(iterable: Iterable, r: int | None = None) -> tuple:
    return more_itertools.random_permutation(iterable, r)


@Pipe
def random_combination(iterable: Iterable, r: int) -> tuple:
    return more_itertools.random_combination(iterable, r)


@Pipe
def replace(iterable: Iterable, predicate: "function", substitues, count=None) -> tuple:
    return more_itertools.replace(iterable, predicate, substitues, count)


@Pipe
def reversed(iterable: Iterable) -> Iterable:
    return more_itertools.always_reversible(iterable)


@Pipe
def iter(iterable: Iterable) -> Iterable:
    return more_itertools.always_iterable(iterable)


@Pipe
def islice(iterable: Iterable, start: int, stop: int, step: int = None) -> Iterable:
    return more_itertools.islice_extended(iterable, start, stop, step)


@Pipe
def strip(iterable: Iterable, predicate: "function") -> Iterable:
    return more_itertools.strip(iterable, predicate)


@Pipe
def map_except(iterable: Iterable, validator: "function", *exceptions) -> Iterable:
    return more_itertools.map_except(validator, iterable, *exceptions)


@Pipe
def filter_except(iterable: Iterable, validator: "function", *exceptions) -> Iterable:
    return more_itertools.filter_except(validator, iterable, *exceptions)


@Pipe
def nth(iterable: Iterable, n: int) -> Any:
    return more_itertools.nth(iterable, n)


@Pipe
def unique(iterable: Iterable, key: "function | None" = None) -> Iterable:
    return more_itertools.unique_everseen(iterable, key)


@Pipe
def sample(iterable: Iterable, k: int, weights: Iterable | None = None) -> Iterable:
    return more_itertools.sample(iterable, k, weights)


@Pipe
def as_list(iterable: Iterable) -> list:
    return list(iterable)


@Pipe
def as_dict(iterable: Iterable) -> dict:
    return dict(iterable)


@Pipe
def as_set(iterable: Iterable) -> set:
    return set(iterable)


@Pipe
def items(iterable: dict) -> list:
    return iterable.items()


@Pipe
def enumerate(iterable: Iterable) -> Iterable:
    return builtins.enumerate(iterable)


@Pipe
def cycle(iterable: Iterable) -> Iterable:
    return itertools.cycle(iterable)
