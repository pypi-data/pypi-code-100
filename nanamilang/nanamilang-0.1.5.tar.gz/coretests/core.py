"""NanamiLang Core Tests"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

import datetime
import unittest
from typing import List
from nanamilang.token import Token
from nanamilang.program import Program
from nanamilang.tokenizer import Tokenizer
from nanamilang.formatter import Formatter


class TestNanamiLangCore(unittest.TestCase):
    """NanamiLang Core Test Cases here"""

    @staticmethod
    def tokenize(line: str):
        """Shortcut for tokenizing"""
        return Tokenizer(line).tokenize()

    @staticmethod
    def convert(expected: List[Token], actual: List[Token]):
        """Make self.assertEqual working"""
        return [[list(map(lambda t: t.type(), expected)),
                 list(map(lambda t: t.dt().reference() if t.dt() else None, expected))],
                [list(map(lambda t: t.type(), actual)),
                 list(map(lambda t: t.dt().reference() if t.dt() else None, actual))]]

    def test__formatting(self):
        """Test formatting"""
        with open('evaltests/core.nml', encoding='utf-8') as reader:
            _input_ = reader.read()
        expected = '(if (= (type 3) "IntegerNumber") "Works?" "Does not work :("))'
        self.assertEqual(expected, Formatter(Tokenizer(_input_).tokenize()).format())

    def test__tokenize_all_possible_tokens(self):
        """We need to be sure we can tokenize that messy string"""
        expected = [Token(Token.ListBegin),
                    Token(Token.Identifier, "+"),
                    Token(Token.Identifier, 'sample'),
                    Token(Token.IntegerNumber, 0),
                    Token(Token.IntegerNumber, 1),
                    Token(Token.FloatNumber, 2.5),
                    Token(Token.FloatNumber, 2.25),
                    Token(Token.FloatNumber, 31.3),
                    Token(Token.String, ""),
                    Token(Token.String, " "),
                    Token(Token.String, "string"),
                    Token(Token.IntegerNumber, 0),
                    Token(Token.IntegerNumber, 11),
                    Token(Token.IntegerNumber, 22),
                    Token(Token.Boolean, True),
                    Token(Token.Boolean, False),
                    Token(Token.Keyword, 'some-2'),
                    Token(Token.Date, datetime.datetime.fromisoformat('1970-10-10')),
                    Token(Token.IntegerNumber, 333),
                    Token(Token.ListEnd)]
        self.assertEqual(*self.convert(expected, self.tokenize(
            '(+ sample '
            '0 1 2.5 2.25 31.30 "" " " "string" 00 11 22 true false :some-2 #1970-10-10 333)')))

    def test__simple_eval_test(self):
        """Test Builtin.if_ function implementation"""
        self.assertEqual('Equals!', Program('(if (= (+ 2 2) 4) "Equals!" "Not equals!")').evaluate().reference())
