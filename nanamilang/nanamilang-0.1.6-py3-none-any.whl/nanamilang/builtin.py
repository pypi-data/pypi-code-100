"""NanamiLang Builtin Class"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

from typing import List
from functools import reduce
from nanamilang import datatypes
from nanamilang.datatypes import Base, Boolean
from nanamilang.shortcuts import ASSERT_LIST_LENGTH_IS, ASSERT_LIST_LENGTH_IS_EVEN


class BuiltinMacro:
    """NanamiLan Builtin Macro"""

    @staticmethod
    def resolve(mc_name: str) -> dict:
        """NanamiLang, resolve macro by its name"""

    @staticmethod
    def comment_macro(tree_slice: list, ev_func, token_cls) -> list:
        """
        Builtin 'comment' macro implementation

        :param tree_slice: slice of encountered tree
        :param ev_func: reference to recursive evaluation function
        :param token_cls: Token class in case we need it
        :return: converted slice of tree (as this would be expected)
        """

        return [token_cls(token_cls.Identifier, 'identity'), token_cls(token_cls.Nil, 'nil')]

    @staticmethod
    def if_macro(tree_slice: list, ev_func, token_cls) -> list:
        """
        Builtin 'if' macro implementation

        :param tree_slice: slice of encountered tree
        :param ev_func: reference to recursive evaluation function
        :param token_cls: Token class in case we need it
        :return: converted slice of tree (as this would be expected)
        """

        condition, true_branch, else_branch = tree_slice

        if not isinstance(condition, list):
            condition = [token_cls(token_cls.Identifier, 'identity'), condition]
        if not isinstance(true_branch, list):
            true_branch = [token_cls(token_cls.Identifier, 'identity'), true_branch]
        if not isinstance(else_branch, list):
            else_branch = [token_cls(token_cls.Identifier, 'identity'), else_branch]

        return true_branch if ev_func(condition).reference() is True else else_branch


class Builtin:
    """NanamiLang Builtin"""

    @staticmethod
    def resolve(fn_name: str) -> dict:
        """NanamiLang, resolve function by its name"""

    @staticmethod
    def make_set_func(args: List[Base]) -> datatypes.Set:
        """NanamiLang, make NanamiLang.Set data structure"""

        assert isinstance(args, list), 'Must be a type of a Python "list"'
        assert args, 'Could not be an empty collection, at least one Type is required'

        return datatypes.Set(set(args))

    @staticmethod
    def make_vector_func(args: List[Base]) -> datatypes.Vector:
        """NanamiLang, make NanamiLang.Vector data structure"""

        assert isinstance(args, list), 'Must be a type of a Python "list"'
        assert args, 'Could not be an empty collection, at least one Type is required'

        return datatypes.Vector(list(args))

    @staticmethod
    def make_hashmap_func(args: List[Base]) -> datatypes.HashMap:
        """NanamiLang, make NanamiLang.HashMap data structure"""

        assert isinstance(args, list), 'Must be a type of a Python "list"'
        assert args, 'Could not be an empty collection, at least one Type is required'
        ASSERT_LIST_LENGTH_IS_EVEN(args)

        pythonic = {}
        idx = 0
        while idx < len(args) - 1:
            pythonic[args[idx]] = args[idx + 1]
            idx += 2

        return datatypes.HashMap(dict(pythonic))

    @staticmethod
    def inc_func(args: (List[datatypes.IntegerNumber] or List[datatypes.FloatNumber])) -> Base:
        """
        Builtin 'dec' function implementation

        :param args: collection of a base instances
        :return: takes 1 argument from list, verify its a number, then return incremented value
        """

        assert isinstance(args, list), 'Must be a type of a Python "list"'
        assert args, 'Could not be an empty collection, at least one Type is required'
        ASSERT_LIST_LENGTH_IS(args, 1)

        arg: Base = args[0]
        assert (isinstance(arg, datatypes.IntegerNumber)
                or isinstance(arg, datatypes.FloatNumber)), (
            'Must be an instance of NanamiLang IntegerNumber or NanamiLang FloatNumber'
        )

        return datatypes.FloatNumber(arg.reference() + 1) if \
            arg.name == datatypes.FloatNumber.name else datatypes.IntegerNumber(arg.reference() + 1)

    @staticmethod
    def dec_func(args: (List[datatypes.IntegerNumber] or List[datatypes.FloatNumber])) -> Base:
        """
        Builtin 'dec' function implementation

        :param args: collection of a base instances
        :return: takes 1 argument from list, verify its a number, then return decremented value
        """

        assert isinstance(args, list), 'Must be a type of a Python "list"'
        assert args, 'Could not be an empty collection, at least one Type is required'
        ASSERT_LIST_LENGTH_IS(args, 1)

        arg: Base = args[0]
        assert (isinstance(arg, datatypes.IntegerNumber)
                or isinstance(arg, datatypes.FloatNumber)), (
            'Must be an instance of NanamiLang IntegerNumber or NanamiLang FloatNumber'
        )

        return datatypes.FloatNumber(arg.reference() - 1) if \
            arg.name == datatypes.FloatNumber.name else datatypes.IntegerNumber(arg.reference() - 1)

    @staticmethod
    def identity_func(args: List[Base]) -> Base:
        """
        Builtin 'identity' function implementation

        :param args: collection of a Base instances
        :return: takes first argument from list and just return it
        """

        assert isinstance(args, list), 'Must be a type of a Python "list"'
        assert args, 'Could not be an empty collection, at least one Type is required'
        ASSERT_LIST_LENGTH_IS(args, 1)

        arg: Base = args[0]

        return arg

    @staticmethod
    def type_func(args: List[Base]) -> datatypes.String:
        """
        Builtin 'type' function implementation

        :param args: collection of a Base instances
        :return: takes first argument from list and return its type name as a String
        """

        assert isinstance(args, list), 'Must be a type of a Python "list"'
        assert args, 'Could not be an empty collection, at least one Type is required'
        ASSERT_LIST_LENGTH_IS(args, 1)

        arg: Base = args[0]

        return datatypes.String(arg.name)

    @staticmethod
    def eq_func(args: List[Base]) -> Boolean:
        """
        Builtin '=' function implementation

        :param args: collection of a Base instances
        :return: comparison result as a Boolean instance
        """

        assert isinstance(args, list), 'Must be a type of a Python "list"'
        assert args, 'Could not be an empty collection, at least one Type is required'
        ASSERT_LIST_LENGTH_IS(args, 2)

        first: Base
        second: Base
        first, second = args

        return Boolean(first.reference() == second.reference())

    @staticmethod
    def lower_than_func(args: (List[datatypes.IntegerNumber]
                               or List[datatypes.FloatNumber])) -> (datatypes.IntegerNumber
                                                                    or datatypes.FloatNumber):
        """
        Builtin '<' function implementation

        :param args: collection of a Base instances
        :return: comparison result as a Boolean instance
        """

        assert isinstance(args, list), 'Must be a type of a Python "list"'
        for arg in args:
            assert isinstance(arg, Base), 'We allow only a Base instances collection'
            assert arg.name \
                   in [datatypes.FloatNumber.name,
                       datatypes.IntegerNumber.name], 'Got invalid Data type'
        assert args, 'Could not be an empty collection, at least one Type is required'
        ASSERT_LIST_LENGTH_IS(args, 2), '"<" function takes only two data type arguments'

        first: Base
        second: Base
        first, second = args

        return Boolean(first.reference() < second.reference())

    @staticmethod
    def greater_than_func(args: (List[datatypes.IntegerNumber]
                                 or List[datatypes.FloatNumber])) -> (datatypes.IntegerNumber
                                                                      or datatypes.FloatNumber):
        """
        Builtin '>' function implementation

        :param args: collection of a Base instances
        :return: comparison result as a Boolean instance
        """

        assert isinstance(args, list), 'Must be a type of a Python "list"'
        for arg in args:
            assert isinstance(arg, Base), 'We allow only a Base instances collection'
            assert arg.name \
                   in [datatypes.FloatNumber.name,
                       datatypes.IntegerNumber.name], 'Got invalid Data type'
        assert args, 'Could not be an empty collection, at least one Type is required'
        ASSERT_LIST_LENGTH_IS(args, 2), '"<" function takes only two data type arguments'

        first: Base
        second: Base
        first, second = args

        return Boolean(first.reference() > second.reference())

    @staticmethod
    def lower_than_eq_func(args: (List[datatypes.IntegerNumber]
                                  or List[datatypes.FloatNumber])) -> (datatypes.IntegerNumber
                                                                       or datatypes.FloatNumber):
        """
        Builtin '<=' function implementation

        :param args: collection of a Base instances
        :return: comparison result as a Boolean instance
        """

        assert isinstance(args, list), 'Must be a type of a Python "list"'
        for arg in args:
            assert isinstance(arg, Base), 'We allow only a Base instances collection'
            assert arg.name \
                   in [datatypes.FloatNumber.name,
                       datatypes.IntegerNumber.name], 'Got invalid Data type'
        assert args, 'Could not be an empty collection, at least one Type is required'
        ASSERT_LIST_LENGTH_IS(args, 2), '"<" function takes only two data type arguments'

        first: Base
        second: Base
        first, second = args

        return Boolean(first.reference() <= second.reference())

    @staticmethod
    def greater_than_eq_func(args: (List[datatypes.IntegerNumber]
                                    or List[datatypes.FloatNumber])) -> (datatypes.IntegerNumber
                                                                         or datatypes.FloatNumber):
        """
        Builtin '>=' function implementation

        :param args: collection of a Base instances
        :return: comparison result as a Boolean instance
        """

        assert isinstance(args, list), 'Must be a type of a Python "list"'
        for arg in args:
            assert isinstance(arg, Base), 'We allow only a Base instances collection'
            assert arg.name \
                   in [datatypes.FloatNumber.name,
                       datatypes.IntegerNumber.name], 'Got invalid Data type'
        assert args, 'Could not be an empty collection, at least one Type is required'
        ASSERT_LIST_LENGTH_IS(args, 2), '"<" function takes only two data type arguments'

        first: Base
        second: Base
        first, second = args

        return Boolean(first.reference() >= second.reference())

    @staticmethod
    def plus_func(args: (List[datatypes.IntegerNumber]
                         or List[datatypes.FloatNumber])) -> (datatypes.IntegerNumber
                                                              or datatypes.FloatNumber):
        """
        Builtin '+' function implementation

        :param args: collection of a Base instances
        :return: "plus" function calculation result
        """

        assert isinstance(args, list), 'Must be a type of a Python "list"'
        for arg in args:
            assert isinstance(arg, Base), 'We allow only a Base instances collection'
            assert arg.name \
                   in [datatypes.FloatNumber.name,
                       datatypes.IntegerNumber.name], 'Got invalid Data type'
        assert args, 'Could not be an empty collection, at least one Type is required'

        result = reduce(lambda _, x: _ + x, list(map(lambda n: n.reference(), args)))

        return datatypes.IntegerNumber(result) if isinstance(result, int) else datatypes.FloatNumber(result)

    @staticmethod
    def minus_func(args: (List[datatypes.IntegerNumber]
                          or List[datatypes.FloatNumber])) -> (datatypes.IntegerNumber
                                                               or datatypes.FloatNumber):
        """
        Builtin '-' function implementation

        :param args: collection of a Base instances
        :return: "minus" function calculation result
        """

        assert isinstance(args, list), 'Must be a type of a Python "list"'
        for arg in args:
            assert isinstance(arg, Base), 'We allow only a Base instances collection'
            assert arg.name \
                   in [datatypes.FloatNumber.name,
                       datatypes.IntegerNumber.name], 'Got invalid Data type'
        assert args, 'Could not be an empty collection, at least one Type is required'

        result = reduce(lambda _, x: _ - x, list(map(lambda n: n.reference(), args)))

        return datatypes.IntegerNumber(result) if isinstance(result, int) else datatypes.FloatNumber(result)

    @staticmethod
    def divide_func(args: (List[datatypes.IntegerNumber]
                           or List[datatypes.FloatNumber])) -> (datatypes.IntegerNumber
                                                                or datatypes.FloatNumber):
        """
        Builtin '/' function implementation

        :param args: collection of a Base instances
        :return: "divide" function calculation result
        """

        assert isinstance(args, list), 'Must be a type of a Python "list"'
        for arg in args:
            assert isinstance(arg, Base), 'We allow only a Base instances collection'
            assert arg.name \
                   in [datatypes.FloatNumber.name,
                       datatypes.IntegerNumber.name], 'Got invalid Data type'
        assert args, 'Could not be an empty collection, at least one Type is required'

        result = reduce(lambda _, x: _ / x, list(map(lambda n: n.reference(), args)))

        return datatypes.IntegerNumber(result) if isinstance(result, int) else datatypes.FloatNumber(result)

    @staticmethod
    def multiply_func(args: (List[datatypes.IntegerNumber]
                             or List[datatypes.FloatNumber])) -> (datatypes.IntegerNumber
                                                                  or datatypes.FloatNumber):
        """
        Builtin '*' function implementation

        :param args: collection of a Base instances
        :return: "multiply" function calculation result
        """
        assert isinstance(args, list), 'Must be a type of a Python "list"'
        for arg in args:
            assert isinstance(arg, Base), 'We allow only a Base instances collection'
            assert arg.name \
                   in [datatypes.FloatNumber.name,
                       datatypes.IntegerNumber.name], 'Got invalid Data type'
        assert args, 'Could not be an empty collection, at least one Type is required'

        result = reduce(lambda _, x: _ * x, list(map(lambda n: n.reference(), args)))

        return datatypes.IntegerNumber(result) if isinstance(result, int) else datatypes.FloatNumber(result)


class Library:
    """NanamiLang Library"""

    macro: dict = {'if': {'macro_name': 'if', 'macro_reference': BuiltinMacro.if_macro},
                   'comment': {'macro_name': 'comment', 'macro_reference': BuiltinMacro.comment_macro}}

    library: dict = {'=': {'function_name': '=',
                           'function_reference': Builtin.eq_func},
                     '+': {'function_name': '+',
                           'function_reference': Builtin.plus_func},
                     '-': {'function_name': '-',
                           'function_reference': Builtin.minus_func},
                     '/': {'function_name': '/',
                           'function_reference': Builtin.divide_func},
                     '*': {'function_name': '*',
                           'function_reference': Builtin.multiply_func},
                     '<': {'function_name': '<',
                           'function_reference': Builtin.lower_than_func},
                     '>': {'function_name': '>',
                           'function_reference': Builtin.greater_than_func},
                     '<=': {'function_name': '<=',
                            'function_reference': Builtin.lower_than_eq_func},
                     '>=': {'function_name': '>=',
                            'function_reference': Builtin.greater_than_eq_func},
                     'inc': {'function_name': 'inc', 'function_reference': Builtin.inc_func},
                     'dec': {'function_name': 'dec', 'function_reference': Builtin.dec_func},
                     'type': {'function_name': 'type', 'function_reference': Builtin.type_func},
                     'identity': {'function_name': 'identity', 'function_reference': Builtin.identity_func},
                     'make-set': {'function_name': 'make-set', 'function_reference': Builtin.make_set_func},
                     'make-vector': {'function_name': 'make-vector', 'function_reference': Builtin.make_vector_func},
                     'make-hashmap': {'function_name': 'make-hashmap', 'function_reference': Builtin.make_hashmap_func}}


Builtin.resolve = lambda function_name: Library.library.get(function_name, None)
BuiltinMacro.resolve = lambda a_macro_name: Library.macro.get(a_macro_name, None)


class Help:
    """NanamiLang Help for builtins"""

    @staticmethod
    def help() -> str:
        """Generates help message"""
        return '\n'.join(Help.docstrings)

    docstrings: List[str] = [
        '(type Base: a) -> String: result',
        '(identity Base: a) -> Base: result',
        '(= Base: a Base: b) -> Boolean: result',
        '(make-set Base: a Base b ...) -> Set: result',
        '(comment ... comment body ...) -> Nil: result',
        '(inc IntegerNumber: a) -> IntegerNumber: result',
        '(dec IntegerNumber: a) -> IntegerNumber: result',
        '(make-vector Base: a Base: b...) -> Vector: result',
        '(make-hashmap Base: a Base: b ...) -> HashMap: result',
        '(if Base: condition Base: on-true Base: on-false) -> Base: result',
        '(fn [... function parameters vector ...] ... function body ...) -> UserDefinedFunction: result',
        '(< (IntegerNumber|FloatNumber): a (IntegerNumber|FloatNumber): b) -> (IntegerNumber|FloatNumber): result',
        '(> (IntegerNumber|FloatNumber): a (IntegerNumber|FloatNumber): b) -> (IntegerNumber|FloatNumber): result',
        '(<= (IntegerNumber|FloatNumber): a (IntegerNumber|FloatNumber): b) -> (IntegerNumber|FloatNumber): result',
        '(>= (IntegerNumber|FloatNumber): a (IntegerNumber|FloatNumber): b) -> (IntegerNumber|FloatNumber): result',
        '(+ (IntegerNumber|FloatNumber): a (IntegerNumber|FloatNumber): b ...) -> (IntegerNumber|FloatNumber): result',
        '(- (IntegerNumber|FloatNumber): a (IntegerNumber|FloatNumber): b ...) -> (IntegerNumber|FloatNumber): result',
        '(/ (IntegerNumber|FloatNumber): a (IntegerNumber|FloatNumber): b ...) -> (IntegerNumber|FloatNumber): result',
        '(* (IntegerNumber|FloatNumber): a (IntegerNumber|FloatNumber): b ...) -> (IntegerNumber|FloatNumber): result']
