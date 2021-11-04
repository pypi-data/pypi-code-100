"""NanamiLang Builtin Class"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

import functools
from typing import List
from functools import reduce
from nanamilang import datatypes
from nanamilang.shortcuts import (
    ASSERT_HAS_KEY, ASSERT_LIST_LENGTH_IS,
    ASSERT_LIST_LENGTH_IS_EVEN, ASSERT_NOT_EMPTY_COLLECTION
)


def meta(meta_: dict):
    """
    NanamiLang, apply meta to func
    'name', 'sample' and 'docstring'

    :param meta_: function meta data
    """
    def wrapped(fn):
        @functools.wraps(fn)
        def function(*args, **kwargs):
            return fn(*args, **kwargs)
        ASSERT_HAS_KEY(meta_, 'name')
        ASSERT_HAS_KEY(meta_, 'sample')
        ASSERT_HAS_KEY(meta_, 'docstring')
        function.meta = meta_
        return function
    return wrapped


class BuiltinMacro:
    """NanamiLan Builtin Macro"""

    @staticmethod
    @meta({'name': 'if',
           'sample': '(if condition true-branch else-branch)',
           'docstring': 'Return true- or else-branch depending on condition'})
    def if_macro(tree_slice: list, ev_func, token_cls) -> list:
        """
        Builtin 'if' macro implementation

        :param tree_slice: slice of encountered tree
        :param ev_func: reference to recursive evaluation function
        :param token_cls: nanamilang.token.Token class
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

    @staticmethod
    @meta({'name': 'comment',
           'sample': '(comment ...)',
           'docstring': 'Turn form into datatypes.Nil'})
    def comment_macro(tree_slice: list, ev_func, token_cls) -> list:
        """
        Builtin 'comment' macro implementation

        :param tree_slice: slice of encountered tree
        :param ev_func: reference to recursive evaluation function
        :param token_cls: nanamilang.token.Token class
        :return: converted slice of tree (as this would be expected)
        """

        return [token_cls(token_cls.Identifier, 'identity'), token_cls(token_cls.Nil, 'nil')]

    @staticmethod
    def resolve(mc_name: str) -> dict:
        """Resolve macro by its name"""

        for macro in BuiltinMacro.functions():
            if macro.meta.get('name') == mc_name:
                return {'macro_name': mc_name, 'macro_reference': macro}

    @staticmethod
    def completions() -> List[str]:
        """Return all possible function names (for completion)"""
        return list(map(lambda f: f.meta.get('name'), BuiltinMacro.functions()))

    @staticmethod
    def names() -> List[str]:
        """Return all possible function names"""

        return list(filter(lambda name: '_macro' in name, BuiltinMacro().__dir__()))

    @staticmethod
    def functions() -> list:
        """Return all possible functions"""

        return list(map(lambda n: getattr(BuiltinMacro, n, None), BuiltinMacro.names()))


class Builtin:
    """NanamiLang Builtin"""

    @staticmethod
    def resolve(fn_name: str) -> dict:
        """Resolve function by its name"""

        for func in Builtin.functions():
            if func.meta.get('name') == fn_name:
                return {'function_name': fn_name, 'function_reference': func}

    @staticmethod
    def completions() -> List[str]:
        """Return all possible function names (for completion)"""
        return list(map(lambda f: f.meta.get('name'), Builtin.functions()))

    @staticmethod
    def names() -> List[str]:
        """Return all possible function names"""

        return list(filter(lambda name: '_func' in name, Builtin().__dir__()))

    @staticmethod
    def functions() -> list:
        """Return all possible functions"""

        return list(map(lambda n: getattr(Builtin, n, None), Builtin.names()))

    @staticmethod
    @meta({'name': 'doc',
           'sample': '(doc function-or-macro)',
           'docstring': 'Return Function or Macro doc as a HashMap'})
    def doc_func(args: List[datatypes.Function or datatypes.Macro]) -> datatypes.HashMap:
        """
        Builtin 'doc' function implementation

        :param args: incoming 'doc' function arguments
        :return: datatypes.HashMap
        """

        ASSERT_NOT_EMPTY_COLLECTION(args)
        ASSERT_LIST_LENGTH_IS(args, 1)

        function_or_macro: datatypes.Function or datatypes.Macro = args[0]

        assert (isinstance(function_or_macro, datatypes.Function)
                or isinstance(function_or_macro, datatypes.Macro)), 'Function or Macro was expected'

        return Builtin.make_hashmap_func([datatypes.Keyword('sample'),
                                          datatypes.String(function_or_macro.reference().meta.get('sample')),
                                          datatypes.Keyword('docstring'),
                                          datatypes.String(function_or_macro.reference().meta.get('docstring'))])

    @staticmethod
    @meta({'name': 'get',
           'sample': '(get collection key-or-index)',
           'docstring': 'Collection item by key or index'})
    def get_func(args: List[datatypes.Base]) -> datatypes.Base:
        """
        Builtin 'get' function implementation

        :param args: incoming 'get' function arguments
        :return: datatypes.Base
        """

        ASSERT_NOT_EMPTY_COLLECTION(args)
        ASSERT_LIST_LENGTH_IS(args, 2)

        collection: datatypes.Vector or datatypes.HashMap
        key_or_index: datatypes.Base

        collection, key_or_index = args

        assert (isinstance(collection, datatypes.Vector)
                or isinstance(collection, datatypes.HashMap)), 'HashMap or Vector was expected'

        if isinstance(collection, datatypes.Vector):
            assert isinstance(key_or_index, datatypes.IntegerNumber), 'IntegerNumber was expected'

        return collection.get(key_or_index)

    @staticmethod
    @meta({'name': 'map',
           'sample': '(map function collection)',
           'docstring': 'Vector of mapped collection items'})
    def map_func(args: List[datatypes.Base]) -> datatypes.Vector:
        """
        Builtin 'map' function implementation

        :param args: incoming 'map' function arguments
        :return: datatypes.Vector
        """

        ASSERT_NOT_EMPTY_COLLECTION(args)
        ASSERT_LIST_LENGTH_IS(args, 2)

        function: datatypes.Function
        collection: datatypes.Vector

        function, collection = args

        assert isinstance(function, datatypes.Function), 'Function was expected'
        assert isinstance(collection, datatypes.Vector), 'Vector was expected'

        return datatypes.Vector(
            list(map(lambda e: function.reference()([e]), collection.reference())))

    @staticmethod
    @meta({'name': 'filter',
           'sample': '(filter function collection)',
           'docstring': 'Vector of filtered collection items'})
    def filter_func(args: List[datatypes.Base]) -> datatypes.Vector:
        """
        Builtin 'filter' function implementation

        :param args: incoming 'filter' function arguments
        :return: datatypes.Vector
        """

        ASSERT_NOT_EMPTY_COLLECTION(args)
        ASSERT_LIST_LENGTH_IS(args, 2)

        function: datatypes.Function
        collection: datatypes.Vector

        function, collection = args

        assert isinstance(function, datatypes.Function), 'Function was expected'
        assert isinstance(collection, datatypes.Vector), 'Vector was expected'

        return datatypes.Vector(
            list(filter(lambda e: function.reference()([e]).reference(), collection.reference())))

    @staticmethod
    @meta({'name': 'even?',
           'sample': '(even? number)',
           'docstring': 'Return whether number is even or not'})
    def is_even_func(args: List[datatypes.Base]) -> datatypes.Boolean:
        """
        Builtin 'even?' function implementation

        :param args: incoming 'even?' function arguments
        :return: datatypes.Boolean
        """

        ASSERT_NOT_EMPTY_COLLECTION(args)
        ASSERT_LIST_LENGTH_IS(args, 1)

        number: datatypes.IntegerNumber or datatypes.FloatNumber = args[0]

        assert (isinstance(number, datatypes.IntegerNumber)
                or isinstance(number, datatypes.FloatNumber)), 'IntegerNumber or FloatNumber was expected'

        return datatypes.Boolean(number.reference() % 2 == 0)

    @staticmethod
    @meta({'name': 'nil?',
           'sample': '(nil? something)',
           'docstring': 'Return whether something is nil or not'})
    def is_nil_func(args: List[datatypes.Base]) -> datatypes.Boolean:
        """
        Builtin 'nil?' function implementation

        :param args: incoming 'nil?' function arguments
        :return: datatypes.Boolean
        """

        ASSERT_NOT_EMPTY_COLLECTION(args)
        ASSERT_LIST_LENGTH_IS(args, 1)

        something: datatypes.Base = args[0]

        return datatypes.Boolean(isinstance(something, datatypes.Nil))

    @staticmethod
    @meta({'name': 'make-set',
           'sample': '(make-set ...)',
           'docstring': 'Create Set data structure'})
    def make_set_func(args: List[datatypes.Base]) -> datatypes.Set:
        """
        Builtin 'make-set' function implementation

        :param args: incoming 'make-set' function arguments
        :return: datatypes.Set
        """

        ASSERT_NOT_EMPTY_COLLECTION(args)

        return datatypes.Set(set(args))

    @staticmethod
    @meta({'name': 'make-vector',
           'sample': '(make-vector ...)',
           'docstring': 'Create Vector data structure'})
    def make_vector_func(args: List[datatypes.Base]) -> datatypes.Vector:
        """
        Builtin 'make-vector' function implementation

        :param args: incoming 'make-vector' function arguments
        :return: datatypes.Vector
        """

        ASSERT_NOT_EMPTY_COLLECTION(args)

        return datatypes.Vector(list(args))

    @staticmethod
    @meta({'name': 'make-hashmap',
           'sample': '(make-hashmap ...)',
           'docstring': 'Create HashMap data structure'})
    def make_hashmap_func(args: List[datatypes.Base]) -> datatypes.HashMap:
        """
        Builtin 'make-hashmap' function implementation

        :param args: incoming 'make-hashmap' function arguments
        :return: datatypes.HashMap
        """

        ASSERT_NOT_EMPTY_COLLECTION(args)
        ASSERT_LIST_LENGTH_IS_EVEN(args)

        pythonic = {}
        idx = 0
        while idx < len(args) - 1:
            pythonic[args[idx]] = args[idx + 1]
            idx += 2

        return datatypes.HashMap(dict(pythonic))

    @staticmethod
    @meta({'name': 'inc',
           'sample': '(inc number)',
           'docstring': 'Return incremented number'})
    def inc_func(args: (List[datatypes.IntegerNumber]
                        or List[datatypes.FloatNumber])) -> (datatypes.IntegerNumber
                                                             or datatypes.FloatNumber):
        """
        Builtin 'inc' function implementation

        :param args: incoming 'inc' function arguments
        :return: datatypes.IntegerNumber or datatypes.FloatNumber
        """

        ASSERT_NOT_EMPTY_COLLECTION(args)
        ASSERT_LIST_LENGTH_IS(args, 1)

        number: (datatypes.IntegerNumber or datatypes.FloatNumber) = args[0]
        assert (isinstance(number, datatypes.IntegerNumber)
                or isinstance(number, datatypes.FloatNumber)), 'IntegerNumber or FloatNumber was expected'
        return datatypes.IntegerNumber(number.reference() + 1) if \
            isinstance(number, datatypes.IntegerNumber) else datatypes.FloatNumber(number.reference() + 1)

    @staticmethod
    @meta({'name': 'dec',
           'sample': '(dec number)',
           'docstring': 'Return decremented number'})
    def dec_func(args: (List[datatypes.IntegerNumber]
                        or List[datatypes.FloatNumber])) -> (datatypes.IntegerNumber
                                                             or datatypes.FloatNumber):
        """
        Builtin 'dec' function implementation

        :param args: incoming 'dec' function arguments
        :return: datatypes.IntegerNumber or datatypes.FloatNumber
        """

        ASSERT_NOT_EMPTY_COLLECTION(args)
        ASSERT_LIST_LENGTH_IS(args, 1)

        number: (datatypes.IntegerNumber or datatypes.FloatNumber) = args[0]
        assert (isinstance(number, datatypes.IntegerNumber)
                or isinstance(number, datatypes.FloatNumber)), 'IntegerNumber or FloatNumber was expected'
        return datatypes.IntegerNumber(number.reference() - 1) if \
            isinstance(number, datatypes.IntegerNumber) else datatypes.FloatNumber(number.reference() - 1)

    @staticmethod
    @meta({'name': 'identity',
           'sample': '(identity something)',
           'docstring': 'Just return something'})
    def identity_func(args: List[datatypes.Base]) -> datatypes.Base:
        """
        Builtin 'identity' function implementation

        :param args: incoming 'identity' function arguments
        :return: datatypes.Base
        """

        ASSERT_NOT_EMPTY_COLLECTION(args)
        ASSERT_LIST_LENGTH_IS(args, 1)

        something: datatypes.Base = args[0]

        return something

    @staticmethod
    @meta({'name': 'type',
           'sample': '(type something)',
           'docstring': 'Return something type name as a String'})
    def type_func(args: List[datatypes.Base]) -> datatypes.String:
        """
        Builtin 'type' function implementation

        :param args: incoming 'type' function arguments
        :return: datatypes.String
        """

        ASSERT_NOT_EMPTY_COLLECTION(args)
        ASSERT_LIST_LENGTH_IS(args, 1)

        something: datatypes.Base = args[0]

        return datatypes.String(something.name)

    @staticmethod
    @meta({'name': '=',
           'sample': '(= f s)',
           'docstring': 'Whether f equals to s or not'})
    def eq_func(args: List[datatypes.Base]) -> datatypes.Boolean:
        """
        Builtin '=' function implementation

        :param args: incoming '=' function arguments
        :return: datatypes.Boolean
        """

        ASSERT_NOT_EMPTY_COLLECTION(args)
        ASSERT_LIST_LENGTH_IS(args, 2)

        f: datatypes.Base
        s: datatypes.Base
        f, s = args

        return datatypes.Boolean(f.reference() == s.reference())

    @staticmethod
    @meta({'name': '<',
           'sample': '(< f s)',
           'docstring': 'Whether f lower than s or not'})
    def lower_than_func(args: (List[datatypes.IntegerNumber]
                               or List[datatypes.FloatNumber])) -> datatypes.Boolean:
        """
        Builtin '<' function implementation

        :param args: incoming '<' function arguments
        :return: datatypes.Boolean
        """

        ASSERT_NOT_EMPTY_COLLECTION(args)
        ASSERT_LIST_LENGTH_IS(args, 2)
        for arg in args:
            assert (isinstance(arg, datatypes.IntegerNumber)
                    or isinstance(arg, datatypes.FloatNumber)), 'IntegerNumber or FloatNumber were expected'

        f: datatypes.IntegerNumber or datatypes.FloatNumber
        s: datatypes.IntegerNumber or datatypes.FloatNumber
        f, s = args

        return datatypes.Boolean(f.reference() < s.reference())

    @staticmethod
    @meta({'name': '>',
           'sample': '(> f s)',
           'docstring': 'Whether f greater than s or not'})
    def greater_than_func(args: (List[datatypes.IntegerNumber]
                                 or List[datatypes.FloatNumber])) -> datatypes.Boolean:
        """
        Builtin '>' function implementation

        :param args: incoming '>' function arguments
        :return: datatypes.Boolean
        """

        ASSERT_NOT_EMPTY_COLLECTION(args)
        ASSERT_LIST_LENGTH_IS(args, 2)
        for arg in args:
            assert (isinstance(arg, datatypes.IntegerNumber)
                    or isinstance(arg, datatypes.FloatNumber)), 'IntegerNumber or FloatNumber were expected'

        f: datatypes.IntegerNumber or datatypes.FloatNumber
        s: datatypes.IntegerNumber or datatypes.FloatNumber
        f, s = args

        return datatypes.Boolean(f.reference() > s.reference())

    @staticmethod
    @meta({'name': '<=',
           'sample': '(<= f s)',
           'docstring': 'Whether f lower than or equals to s or not'})
    def lower_than_eq_func(args: (List[datatypes.IntegerNumber]
                                  or List[datatypes.FloatNumber])) -> datatypes.Boolean:
        """
        Builtin '<=' function implementation

        :param args: incoming '>=' function arguments
        :return: datatypes.Boolean
        """

        ASSERT_NOT_EMPTY_COLLECTION(args)
        ASSERT_LIST_LENGTH_IS(args, 2)
        for arg in args:
            assert (isinstance(arg, datatypes.IntegerNumber)
                    or isinstance(arg, datatypes.FloatNumber)), 'IntegerNumber or FloatNumber were expected'

        f: datatypes.IntegerNumber or datatypes.FloatNumber
        s: datatypes.IntegerNumber or datatypes.FloatNumber
        f, s = args

        return datatypes.Boolean(f.reference() <= s.reference())

    @staticmethod
    @meta({'name': '>=',
           'sample': '(>= f s)',
           'docstring': 'Whether f greater than or equals to s or not'})
    def greater_than_eq_func(args: (List[datatypes.IntegerNumber]
                                    or List[datatypes.FloatNumber])) -> datatypes.Boolean:
        """
        Builtin '>=' function implementation

        :param args: incoming '>=' function arguments
        :return: datatypes.Boolean
        """

        ASSERT_NOT_EMPTY_COLLECTION(args)
        ASSERT_LIST_LENGTH_IS(args, 2)
        for arg in args:
            assert (isinstance(arg, datatypes.IntegerNumber)
                    or isinstance(arg, datatypes.FloatNumber)), 'IntegerNumber or FloatNumber were expected'

        f: datatypes.IntegerNumber or datatypes.FloatNumber
        f: datatypes.IntegerNumber or datatypes.FloatNumber
        f, s = args

        return datatypes.Boolean(f.reference() >= s.reference())

    @staticmethod
    @meta({'name': '+',
           'sample': '(+ ...)',
           'docstring': 'All passed numbers summary'})
    def plus_func(args: (List[datatypes.IntegerNumber]
                         or List[datatypes.FloatNumber])) -> (datatypes.IntegerNumber
                                                              or datatypes.FloatNumber):
        """
        Builtin '+' function implementation

        :param args: incoming '+' function arguments
        :return: datatypes.IntegerNumber or datatypes.FloatNumber
        """

        ASSERT_NOT_EMPTY_COLLECTION(args)
        for arg in args:
            assert (isinstance(arg, datatypes.IntegerNumber)
                    or isinstance(arg, datatypes.FloatNumber)), 'IntegerNumber or FloatNumber were expected'

        result = reduce(lambda _, x: _ + x, list(map(lambda n: n.reference(), args)))

        return datatypes.IntegerNumber(result) if isinstance(result, int) else datatypes.FloatNumber(result)

    @staticmethod
    @meta({'name': '-',
           'sample': '(- ...)',
           'docstring': 'All passed numbers difference'})
    def minus_func(args: (List[datatypes.IntegerNumber]
                          or List[datatypes.FloatNumber])) -> (datatypes.IntegerNumber
                                                               or datatypes.FloatNumber):
        """
        Builtin '-' function implementation

        :param args: incoming '-' function arguments
        :return: datatypes.IntegerNumber or datatypes.FloatNumber
        """

        ASSERT_NOT_EMPTY_COLLECTION(args)
        for arg in args:
            assert (isinstance(arg, datatypes.IntegerNumber)
                    or isinstance(arg, datatypes.FloatNumber)), 'IntegerNumber or FloatNumber were expected'

        result = reduce(lambda _, x: _ - x, list(map(lambda n: n.reference(), args)))

        return datatypes.IntegerNumber(result) if isinstance(result, int) else datatypes.FloatNumber(result)

    @staticmethod
    @meta({'name': '/',
           'sample': '(/ ...)',
           'docstring': 'All passed numbers division'})
    def divide_func(args: (List[datatypes.IntegerNumber]
                           or List[datatypes.FloatNumber])) -> (datatypes.IntegerNumber
                                                                or datatypes.FloatNumber):
        """
        Builtin '/' function implementation

        :param args: incoming '/' function arguments
        :return: datatypes.IntegerNumber or datatypes.FloatNumber
        """

        ASSERT_NOT_EMPTY_COLLECTION(args)
        for arg in args:
            assert (isinstance(arg, datatypes.IntegerNumber)
                    or isinstance(arg, datatypes.FloatNumber)), 'IntegerNumber or FloatNumber were expected'

        result = reduce(lambda _, x: _ / x, list(map(lambda n: n.reference(), args)))

        return datatypes.IntegerNumber(result) if isinstance(result, int) else datatypes.FloatNumber(result)

    @staticmethod
    @meta({'name': '*',
           'sample': '(* ...)',
           'docstring': 'All passed numbers production'})
    def multiply_func(args: (List[datatypes.IntegerNumber]
                             or List[datatypes.FloatNumber])) -> (datatypes.IntegerNumber
                                                                  or datatypes.FloatNumber):
        """
        Builtin '*' function implementation

        :param args: incoming '*' function arguments
        :return: datatypes.IntegerNumber or datatypes.FloatNumber
        """

        ASSERT_NOT_EMPTY_COLLECTION(args)
        for arg in args:
            assert (isinstance(arg, datatypes.IntegerNumber)
                    or isinstance(arg, datatypes.FloatNumber)), 'IntegerNumber or FloatNumber were expected'

        result = reduce(lambda _, x: _ * x, list(map(lambda n: n.reference(), args)))

        return datatypes.IntegerNumber(result) if isinstance(result, int) else datatypes.FloatNumber(result)
