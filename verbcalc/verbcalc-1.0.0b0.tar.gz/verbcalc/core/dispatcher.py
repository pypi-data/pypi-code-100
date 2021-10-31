"""
Dispatches single step operations in correct order.
"""
import operator


class Dispatcher:
    """
    Dispatches single step operations according to given rules.

    Attributes:
        arithmetic_operations:
            Dictionary containing string representation of arithmetic
            operators along with their callables.
    """

    def __init__(self):
        self.arithmetic_operations = {'**': operator.pow,
                                      '*': operator.mul,
                                      '/': operator.truediv,
                                      '+': operator.add,
                                      '-': operator.sub}
        self.functions = {'abs': operator.abs}

    def dispatch(self, tokens: list) -> float:
        """
        Dispatches all the operations.

        Arguments:
            tokens:
                List containing all the tokens.

        Raises:
            ZeroDivisionError: Calculation requires dividing by zero, which
                               makes small puppies die.

            InvalidExpressionException: Raised when expression contains stuff
                                        like ['2', '4'] or ['-', '/']

        Returns:
            Result of calculation.
        """
        while len(tokens) > 1:
            last_length = len(tokens)
            for rule in self.arithmetic_operations.items():
                try:
                    i = tokens.index(rule[0])
                    tokens[i] = str(
                        rule[1](float(tokens[i - 1]),
                                float(tokens[i + 1])))
                    del tokens[i - 1]
                    del tokens[i]
                except ValueError:
                    pass
            for fun in self.functions.items():
                try:
                    i = tokens.index(fun[0])
                    # noinspection PyTypeChecker
                    tokens[i] = str(
                        fun[1](float(tokens[i + 1])))
                    del tokens[i + 1]
                except ValueError:
                    pass
            if len(tokens) is last_length:
                raise InvalidExpressionException
        return float(tokens[0])


class InvalidExpressionException(Exception):
    """
    Raised when expression is invalid (for example contains 2 arithmetic
    operators in a row).
    """
