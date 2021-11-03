"""NanamiLang Shortcuts"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)


from typing import Any


def get_var_name(v: Any) -> str:
    """get a variable name"""
    return f'{v=}'.split('=')[0]


def UNTERMINATED_SYMBOL(sym: str):
    """UNTERMINATED_SYMBOL(sym) -> message"""
    return f'Encountered an unterminated \'{sym}\' symbol'


def UNTERMINATED_SYMBOL_AT_EOF(sym: str):
    """UNTERMINATED_SYMBOL_AT_EOF(sym) -> message"""
    return f'Encountered an unterminated symbol \'{sym}\' symbol at the end of file'


def ASSERT_NOT_EMPTY_STRING(s: str) -> None:
    """ASSERT_NOT_EMPTY_STRING(s) -> assertion with a message"""
    assert s, f'"{get_var_name(s)}" could not be an empty string'


def ASSERT_LIST_LENGTH_IS(c: list, l: int) -> None:
    """ASSERT_LIST_LENGTH_IS(c, l) -> assertion with a message"""
    assert len(c) == l, f'{get_var_name(c)} must be length of {l}'


def ASSERT_LIST_LENGTH_IS_EVEN(c: list) -> None:
    """AASSERT_LIST_LENGTH_IS_EVEN(c) -> assertion with a message"""
    assert len(c) % 2 == 0, f'{get_var_name(c)} length must be even'


def ASSERT_NOT_EMPTY_COLLECTION(c: (list or dict)) -> None:
    """ASSERT_NOT_EMPTY_COLLECTION(c) -> assertion with a message"""
    assert c, f'"{get_var_name(c)}" could not be an empty collection'


def ASSERT_HAS_KEY(v: dict, k: str) -> None:
    """ASSERT_HAS_KEY(v, k) -> assertion with a message"""
    assert v.get(k), f'"{(get_var_name(v))}" must have a "{get_var_name(k)}" key'


def ASSERT_TYPE_OF_A(v: Any, t: Any) -> None:
    """ASSERT_TYPE_OF_A(v, t) -> assertion with a message"""
    assert isinstance(v, t), f'"{get_var_name(v)}" must be a type of a "{t.__name__}"'


def ASSERT_IN(v: Any, c: list) -> None:
    """ASSERT_IN(v, c) -> assertion with a message"""
    assert v in c, f'You have picked wrong "{get_var_name(v)}", choose from these: "{c}"'
