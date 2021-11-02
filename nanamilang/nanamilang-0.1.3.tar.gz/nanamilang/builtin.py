"""NanamiLang Builtin Class"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

from typing import List
from nanamilang import datatypes
from nanamilang.datatypes import Base, Boolean
from nanamilang.shortcuts import ASSERT_LIST_LENGTH_IS, ASSERT_LIST_LENGTH_IS_EVEN


class Builtin:
    """NanamiLang Builtin"""

    @staticmethod
    def resolve(fn_name: str) -> dict:
        """NanamiLang, resolve function by its name"""

    @staticmethod
    def make_set(args: List[Base]) -> datatypes.Set:
        """NanamiLang, make NanamiLang.Set data structure"""

        assert isinstance(args, list), 'Must be a type of a Python "list"'
        assert args, 'Could not be an empty collection, at least one Type is required'

        return datatypes.Set(set(args))

    @staticmethod
    def make_vector(args: List[Base]) -> datatypes.Vector:
        """NanamiLang, make NanamiLang.Vector data structure"""

        assert isinstance(args, list), 'Must be a type of a Python "list"'
        assert args, 'Could not be an empty collection, at least one Type is required'

        return datatypes.Vector(list(args))

    @staticmethod
    def make_hashmap(args: List[Base]) -> datatypes.HashMap:
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
        """NanamiLang, 'inc' function implementation"""

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
        """NanamiLang, 'dec' function implementation"""

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
    def identity(args: List[Base]) -> Base:
        """NanamiLang, 'identity' function implementation"""

        assert isinstance(args, list), 'Must be a type of a Python "list"'
        assert args, 'Could not be an empty collection, at least one Type is required'
        ASSERT_LIST_LENGTH_IS(args, 1)

        arg: Base = args[0]

        return arg

    @staticmethod
    def data_type_name(args: List[Base]) -> datatypes.String:
        """NanamiLang, 'type' function implementation"""

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
    def if_func(args: List[Base]) -> Base:
        """
        Builtin 'if' function implementation

        :param args: collection of a Base instances
        :return: comparison result as a Boolean instance
        """

        assert isinstance(args, list), 'Must be a type of a Python "list"'
        assert args, 'Could not be an empty collection, at least one Type is required'
        ASSERT_LIST_LENGTH_IS(args, 3)

        first: Boolean
        second: Base
        third: Base
        first, second, third = args

        return second if first.reference() is True else third

    @staticmethod
    def lower_than_func(args: List[Base]) -> Boolean:
        """
        Builtin '<' function implementation

        :param args: collection of a Base instances
        :return: comparison result as a Boolean instance
        """

        assert isinstance(args, list), 'Must be a type of a Python "list"'
        assert args, 'Could not be an empty collection, at least one Type is required'
        ASSERT_LIST_LENGTH_IS(args, 2)

        first: Base
        second: Base
        first, second = args

        return Boolean(first.reference() < second.reference())

    @staticmethod
    def greater_than_func(args: List[Base]) -> Boolean:
        """
        Builtin '>' function implementation

        :param args: collection of a Base instances
        :return: comparison result as a Boolean instance
        """

        assert isinstance(args, list), 'Must be a type of a Python "list"'
        assert args, 'Could not be an empty collection, at least one Type is required'
        ASSERT_LIST_LENGTH_IS(args, 2)

        first: Base
        second: Base
        first, second = args

        return Boolean(first.reference() > second.reference())

    @staticmethod
    def lower_than_eq_func(args: List[Base]) -> Boolean:
        """
        Builtin '<=' function implementation

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
    def greater_than_eq_func(args: List[Base]) -> Boolean:
        """
        Builtin '>=' function implementation

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
    def plus_func(args: list[Base]) -> Base:
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

        pythonic = list(map(lambda n: n.reference(), args))

        initial = pythonic[0]
        for arg in pythonic[1:]:
            initial += arg

        return datatypes.IntegerNumber(initial) if isinstance(initial, int) else datatypes.FloatNumber(initial)

    @staticmethod
    def minus_func(args: List[Base]) -> Base:
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

        pythonic = list(map(lambda n: n.reference(), args))

        initial = pythonic[0]
        for arg in pythonic[1:]:
            initial -= arg

        return datatypes.IntegerNumber(initial) if isinstance(initial, int) else datatypes.FloatNumber(initial)

    @staticmethod
    def divide_func(args: List[Base]) -> Base:
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

        pythonic = list(map(lambda n: n.reference(), args))

        initial = pythonic[0]
        for arg in pythonic[1:]:
            initial /= arg

        return datatypes.IntegerNumber(initial) if isinstance(initial, int) else datatypes.FloatNumber(initial)

    @staticmethod
    def multiply_func(args: [Base]) -> Base:
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

        pythonic = list(map(lambda n: n.reference(), args))

        initial = pythonic[0]
        for arg in pythonic[1:]:
            initial *= arg

        return datatypes.IntegerNumber(initial) if isinstance(initial, int) else datatypes.FloatNumber(initial)


class Library:
    """NanamiLang Library"""

    library: dict = {'=': {'function_name': '=',
                           'function_reference': Builtin.eq_func},
                     'if': {'function_name': 'if',
                            'function_reference': Builtin.if_func},
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
                     'type': {'function_name': 'type', 'function_reference': Builtin.data_type_name},
                     'identity': {'function_name': 'identity', 'function_reference': Builtin.identity},
                     'make-set': {'function_name': 'make-set', 'function_reference': Builtin.make_set},
                     'make-vector': {'function_name': 'make-vector', 'function_reference': Builtin.make_vector},
                     'make-hashmap': {'function_name': 'make-hashmap', 'function_reference': Builtin.make_hashmap}}


Builtin.resolve = lambda function_name: Library.library.get(function_name, None)


class Help:
    """NanamiLang Help for builtins"""

    @staticmethod
    def help() -> str:
        """Generates help message"""
        return '\n'.join(Help.docstrings)

    docstrings: List[str] = [
        '(make-set Base: a Base b ...) -> Set: result',
        '(make-vector Base: a Base: b...) -> Vector: result',
        '(make-hashmap Base: a Base: b ...) -> HashMap: result',
        '(type Base: a) -> String: result',
        '(identity Base: a) -> Base: result',
        '(= Base: a Base: b) -> Boolean: result',
        '(inc IntegerNumber: a) -> IntegerNumber: result',
        '(dec IntegerNumber: a) -> IntegerNumber: result',
        '(if Base: condition Base: on-true Base: on-false) -> Base: result',
        '(< (IntegerNumber|FloatNumber): a (IntegerNumber|FloatNumber): b) -> (IntegerNumber|FloatNumber): result',
        '(> (IntegerNumber|FloatNumber): a (IntegerNumber|FloatNumber): b) -> (IntegerNumber|FloatNumber): result',
        '(<= (IntegerNumber|FloatNumber): a (IntegerNumber|FloatNumber): b) -> (IntegerNumber|FloatNumber): result',
        '(>= (IntegerNumber|FloatNumber): a (IntegerNumber|FloatNumber): b) -> (IntegerNumber|FloatNumber): result',
        '(+ (IntegerNumber|FloatNumber): a (IntegerNumber|FloatNumber): b ...) -> (IntegerNumber|FloatNumber): result',
        '(- (IntegerNumber|FloatNumber): a (IntegerNumber|FloatNumber): b ...) -> (IntegerNumber|FloatNumber): result',
        '(/ (IntegerNumber|FloatNumber): a (IntegerNumber|FloatNumber): b ...) -> (IntegerNumber|FloatNumber): result',
        '(* (IntegerNumber|FloatNumber): a (IntegerNumber|FloatNumber): b ...) -> (IntegerNumber|FloatNumber): result']
