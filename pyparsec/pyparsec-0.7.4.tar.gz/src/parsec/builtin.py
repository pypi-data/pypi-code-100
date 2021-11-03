class Combinator:
    def __init__(self, parsec):
        self.parsec = parsec

    def __call__(self, st):
        return self.parsec(st)

    def bind(self, continuation):
        return self.parsec.bind(continuation)

    def then(self, p):
        return self.parsec.then(p)

    def over(self, p):
        return self.parsec.over(p)


class BuiltIn(Combinator):
    def __init__(self, parsec):
        super().__init__(parsec)
        self.parsec = parsec

    @property
    def head(self):
        from .combinator import ahead
        return ahead(self.parsec)

    @property
    def attempt(self):
        from .combinator import attempt
        return attempt(self.parsec)

    @property
    def many(self):
        from .combinator import many
        return many(self.parsec)

    @property
    def many1(self):
        from .combinator import many1
        return many1(self.parsec)

    @property
    def skip(self):
        from .combinator import skip
        return skip(self.parsec)

    @property
    def skip1(self):
        from .combinator import skip1
        return skip1(self.parsec)

    def sepBy(self, by):
        from .combinator import sep
        return sep(self.parsec, by)

    def sepBy1(self, by):
        from .combinator import sep1
        return sep1(self.parsec, by)

    def otherwise(self, other):
        from .combinator import choice
        return choice(self.parsec.attempt, other)

    def manyTill(self, end):
        from .combinator import manyTill
        return manyTill(self.parsec, end)
