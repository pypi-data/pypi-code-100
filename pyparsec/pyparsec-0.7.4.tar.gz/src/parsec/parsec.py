#!/usr/bin/env python3
# coding:utf-8

from .builtin import BuiltIn


class Parsec(BuiltIn):
    def __init__(self, parsec):
        super().__init__(parsec)
        self.parsec = BuiltIn(parsec)

    def __call__(self, st):
        return self.parsec(st)

    def bind(self, continuation):
        def bind(st):
            binder = continuation(self.parsec(st))
            return binder(st)

        return Parsec(bind)

    def then(self, p):
        def then(st):
            self.parsec(st)
            return p(st)

        return Parsec(then)

    def over(self, p):
        def over(st):
            re = self.parsec(st)
            p(st)
            return re

        return Parsec(over)
