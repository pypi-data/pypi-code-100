"""
Translator module allows to change natural language to mathematical notation.
"""
from verbcalc.core.symbols import Symbols

DEFAULT_SYMBOLS = Symbols()


def translate(sentence: str, symbols: Symbols = DEFAULT_SYMBOLS) -> str:
    """
      Translates maths related words into their symbols.

      Args:
          sentence: Sentence to be converted.
          symbols: Instance of symbols to match the words from.

      Returns:
          Converted sentence.
    """
    result = sentence.lower()

    for key in symbols.symbol_dictionary.keys():
        for phrase in symbols.symbol_dictionary[key]:
            result = result.replace(phrase, key)

    return result
