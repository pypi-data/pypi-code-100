"""NanamiLang Program Class"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

from typing import List
from nanamilang.ast import AST
from nanamilang.token import Token
from nanamilang.datatypes import Base
from nanamilang.tokenizer import Tokenizer
from nanamilang.formatter import Formatter
from nanamilang.shortcuts import ASSERT_TYPE_OF_A, ASSERT_NOT_EMPTY_STRING


class Program:
    """
    NanamiLang Program

    ```
    from nanamilang import Program, datatypes
    source: str = '(+ 2 2 (* 2 2))'
    program: Program = Program(str(source)))
    # Program.__init__() method will automatically tokenize am input and build an AST
    program.tokenized() # => will return your a collection of a Token instances
    program.format() # => will return formatted string (but without a syntax sugar)
    program.evaluate() # => will evaluate your program and return a DataType instance
    ````
    """

    _ast: AST = None
    _source: str = None
    _tokenized: List[Token] = None

    def __init__(self, source: str) -> None:
        """
        Initialize a new NanamiLang Program instance

        :param source: your NanamiLang program source code
        """

        ASSERT_TYPE_OF_A(source, str)
        ASSERT_NOT_EMPTY_STRING(source)

        self._source = source
        self._tokenized = Tokenizer(self._source).tokenize()
        self._ast = AST(self._tokenized)

    def dump_tree(self) -> None:
        """NanamiLang Program, dump program AST"""

        def recursive_dump(tree, indent=1) -> None:
            for i in tree:
                if isinstance(i, list):
                    return recursive_dump(i, indent * 4)
                else:
                    print(f'{indent * " "}{i} ({i.dt()})')

        recursive_dump(self.tree())

    def tree(self) -> list:
        """NanamiLang Program, call self._ast.tree()"""

        return self._ast.tree()

    def tokenized(self) -> List[Token]:
        """NanamiLang Program, self._tokenized getter"""

        return self._tokenized

    def format(self) -> str:
        """NanamiLang Program, call Formatter(self._tokenized).format()"""

        return Formatter(self._tokenized).format()

    def evaluate(self) -> Base:
        """NanamiLang Program, call self._ast.evaluate() to evaluate your program"""

        return self._ast.evaluate()
