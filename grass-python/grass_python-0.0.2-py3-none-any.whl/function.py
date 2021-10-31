from typing import TypeVar, Callable

A = TypeVar('A')
B = TypeVar('B')

C = TypeVar('C')

def flip(f: Callable[[A, B], C]) -> Callable[[B, A], C]:
    '''flip'''
    return lambda b,a: f(a, b) 

def const(a: A, _: B) -> A:
    return a

def apply(f: Callable[[A], B], a: A) -> B:
    return f(a)

applyFlipped = flip(apply)

def applyN(f: Callable[[A], A], time: int, a: A) -> A:
    if time <= 0:
        return a
    acc = time
    for _ in range(time):
        acc = f(acc)
    return acc

def id(a: A) -> A :
    return a

def on(ap: Callable[[B,B],C], f: Callable[[A],B], a1:A, a2:A)->C:
    return ap(f(a1), f(a2))

def compose(f: Callable[[B], C], g: Callable[[A], B]) -> Callable[[A], C] :
    return lambda x: f(g(x))