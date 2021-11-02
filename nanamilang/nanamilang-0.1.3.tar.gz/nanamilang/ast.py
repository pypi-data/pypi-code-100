"""NanamiLang AST CLass"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

from typing import List
from nanamilang import datatypes
from nanamilang.token import Token
from nanamilang.shortcuts import ASSERT_NOT_EMPTY_COLLECTION


class ASTException(Exception):
    """NanamiLang AST Exception for any case"""


class AST:
    """
    NanamiLang AST (abstract syntax tree) Generator

    Usage:
    ```
    from nanamilang import AST, Tokenizer, datatypes
    t: Tokenizer = Tokenizer('(+ 2 2 (* 2 2))')
    tokenized = t.tokenize() # => tokenize input string
    ast: AST = AST(tokenized) # => create new AST instance
    result: datatypes.Base = ast.evaluate() # => <IntegerNumber>: 8
    ```
    """

    _tree: list = None
    _tokenized: List[Token] = None

    def __init__(self, tokenized: List[Token]) -> None:
        """Initialize a new NanamiLang AST instance"""

        ASSERT_NOT_EMPTY_COLLECTION(tokenized)

        self._tokenized = tokenized
        self._tree = self._make_tree()

    def tree(self) -> list:
        """NanamiLang AST, self._tree getter"""

        return self._tree

    def _make_tree(self) -> list:
        """NanamiLang AST, make an actual tree"""

        # Written by @buzzer13 (https://gitlab.com/buzzer13)

        # TODO: I need to better understand how it works O.O, thank you Michael

        items = []
        stack = [items]

        for token in self._tokenized:

            if token.type() == Token.ListBegin:

                wired = []
                stack[-1].append(wired)
                stack.append(wired)

            elif token.type() == Token.ListEnd:

                stack.pop()

            else:
                stack[-1].append(token)

        # Added by @jedi2light to support echoing datatypes
        if not isinstance(items[0], list):
            return [Token(Token.Function, 'identity'), items[0]]
        return items[0]

    def evaluate(self) -> datatypes.Base:
        """NanamiLang AST, recursively evaluate tree"""

        def recursive_evaluate(tree: list) -> (datatypes.Base or Token):
            func: (list or Token)
            arguments: list
            func, *arguments = tree
            ready: list = []
            argument: (Token or list)
            for argument in arguments:
                if isinstance(argument, Token):
                    ready.append(argument.dt())
                elif isinstance(argument, list):
                    ready.append(recursive_evaluate(argument))
            if isinstance(func, datatypes.Function):
                return func.reference()(ready)
            elif isinstance(func, Token):
                return func.dt().reference()(ready)
            elif isinstance(func, list):
                return recursive_evaluate(func).reference()(ready)

        return recursive_evaluate(self._tree)
