"""NanamiLang Token Class"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

from typing import Any, List
from nanamilang import datatypes
from nanamilang.builtin import Builtin, BuiltinMacro
from nanamilang.shortcuts import (
    ASSERT_IN, ASSERT_TYPE_OF_A, ASSERT_NOT_EMPTY_STRING
)


class Token:
    """NanamiLang Token"""

    _type: str = None
    _valid: bool = True
    _reason: str = None
    _position: int = None
    _raw_symbol: str = None
    _dt_instance: datatypes.Base = None

    Invalid: str = 'Invalid'
    ListBegin: str = 'ListBegin'
    ListEnd: str = 'ListEnd'
    Identifier: str = 'Identifier'
    Nil: str = datatypes.Nil.name
    Boolean: str = datatypes.Boolean.name
    String: str = datatypes.String.name
    Date: str = datatypes.Date.name
    FloatNumber: str = datatypes.FloatNumber.name
    IntegerNumber: str = datatypes.IntegerNumber.name
    Keyword: str = datatypes.Keyword.name

    meta_types: List[str] = datatypes.DataType.simple_types+[Identifier]

    _valid_types: List[str] = [Invalid, ListBegin, ListEnd] + meta_types

    def __init__(self,
                 _type: str, _value: Any = None,
                 _valid: bool = True, _reason: str = None,
                 _position: int = None, _raw_symbol: str = None) -> None:
        """
        Initialize a new NanamiLang Token instance

        On __init__, will try to initialize respective DataType instance.

        :param _type: must be a Token.<something>
        :param _value: must be a type of a "_type"
        :param _valid: whether Token is valid or not
        :param _reason: reason why token is invalid?
        :param _position: source position of a symbol
        :param _raw_symbol: this must be a raw symbol
        """

        # _type must be a type of str and could not be an empty string
        ASSERT_TYPE_OF_A(_type, str)
        ASSERT_NOT_EMPTY_STRING(_type)
        # _type could not be something different from self._valid_types
        ASSERT_IN(_type, self._valid_types)
        self._type = _type
        # if _type is something from NanamiLang Data Types, initialize it
        if _type in self.meta_types:
            if _type != Token.Identifier:
                self._dt_instance = (
                    datatypes.DataType.resolve(_type)(_value)
                )
            else:
                resolved_fn = Builtin.resolve(_value)
                resolved_mc = BuiltinMacro.resolve(_value)
                if resolved_fn:
                    self._dt_instance = datatypes.Function(resolved_fn)
                elif resolved_mc:
                    self._dt_instance = datatypes.Macro(resolved_mc)
                else:
                    self._dt_instance = datatypes.Undefined(_value)
        # Validate and store passed values for other Token private fields
        if _valid:
            ASSERT_TYPE_OF_A(_valid, bool)
            self._valid = _valid
        if _reason:
            ASSERT_TYPE_OF_A(_reason, str)
            ASSERT_NOT_EMPTY_STRING(_reason)
            self._reason = _reason
        if _position:
            ASSERT_TYPE_OF_A(_position, int)
            self._position = _position
        if _raw_symbol:
            ASSERT_TYPE_OF_A(_raw_symbol, str)
            ASSERT_NOT_EMPTY_STRING(_raw_symbol)
            self._raw_symbol = _raw_symbol

    def type(self) -> str:
        """NanamiLang Token, self._type getter"""

        return self._type

    def dt(self) -> datatypes.Base:
        """NanamiLang Token, self._dt_instance getter"""

        return self._dt_instance

    def __repr__(self) -> str:
        """NanamiLang Token, _repr__() method implementation"""

        return self.__str__()

    def __str__(self) -> str:
        """NanamiLang Token, __str__() method implementation"""

        if self._valid:
            if self._dt_instance is not None:
                return f'<{self._type}>: {self._dt_instance.format()}'
            return f'<{self._type}>'
        return f'Error at the {self._position} position. Reason: {self._reason}'
