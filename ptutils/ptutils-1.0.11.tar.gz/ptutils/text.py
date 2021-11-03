#!/bin/false
# -*- coding: utf-8 -*-

"""
A collection of functions for text manipulation.
"""


# ========================================================================================================================
# Main imports
# ========================================================================================================================
from typing import List


# ========================================================================================================================
# Utility functions: Text manipulation
# ========================================================================================================================


# ------------------------------------------------------------------------------------------------------------------------
def strip_line_ending(text: str) -> str:
    """
    Remove line ending characters from the end of a string.

    Parameters
    ----------
    text : str
        The string to process.

    Returns
    -------
    str
        The string with any trailing '\r' and '\n' characters removed.
    """
    return text.rstrip('\n\r')


# ------------------------------------------------------------------------------------------------------------------------
def strip_quotes(text: str) -> str:
    """
    Remove matching quotation marks from the beginning and ending of a string.

    Parameters
    ----------
    text : str
        The string to process.

    Returns
    -------
    str
        The string with matching leading/trailing quotation marks removed.
    """
    if len(text) < 2:
        return text
    if (text[0] != text[-1]):
        return text
    if text[0] in [ "'", '"' ]:
        return text[1:-1]
    return text


# ------------------------------------------------------------------------------------------------------------------------
def strip_brackets(text: str, brackets: List[ List[ str ] ] = [ ['[', ']'], ['{', '}'], ['(', ')'] ]) -> str:
    """
    Remove opening/closing brackets around a string.

    Parameters
    ----------
    text : str
        The string to process
    brackets : List[ List[ str ] ], optional
        A list of bracket pair definitions, by default [ ['[',']'], ['{','}'], ['(',')'] ]

    Returns
    -------
    str
        The string with any surrounding opening/closing brackets removed.
    """
    if len(text) < 2:
        return text

    for b in brackets:
        if (text[0] == b[0]) and (text[-1] == b[-1]):
            return strip_brackets(text[1:-1])
    return text
