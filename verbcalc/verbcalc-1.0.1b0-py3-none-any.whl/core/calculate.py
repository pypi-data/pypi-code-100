"""
Allows making calculations.
"""
from verbcalc.core.dispatcher import Dispatcher
from verbcalc.core.translator.translator import translate

DEFAULT_DISPATCHER = Dispatcher()


def calculate(sentence: str,
              dispatcher: Dispatcher = DEFAULT_DISPATCHER
              ) -> float:
    """
    Calculates result from sentence.

    Parameters:
        sentence:
            Sentence to take calculation from.

        dispatcher:
            Dispatcher object to use, if none provided it will use default one.

    Returns:
        Calculated sentence.
    """
    return dispatcher.dispatch(translate(sentence).split())
