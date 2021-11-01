import sys
import numpy as np


class Calculator:
    """
    Instantiate a calulator.
    """

    def __init__(self):
        self.previous_result = []
        self.previous_operation = []
        self.previous_input = []
        pass

    def add(self, number1, number2):
        """
        add 2 given number.
        
        :param number1,number2: The numbers to add.
        :type number1,number2: float
    
        :return: The result of the addition.
        :rtype: float
        """
        input = [number1, number2]
        result = np.add(number1, number2)
        self._set_history(input, result)

        return result

    def multiply(self, number1, number2):
        """
        Multiply 2 given number.
        
        :param number1,number2: The numbers to multiply.
        :type number1,number2: float
    
        :return: The result of the multiplication.
        :rtype: float
        """
        input = [number1, number2]
        result = np.dot(number1, number2)
        self._set_history(input, result)

        return result

    def _set_history(self, input, result):
        if len(self.previous_result) > 10:
            self.previous_result.pop(0)
            self.previous_operation.pop(0)
            self.previous_input.pop(0)

        operation = sys._getframe().f_back.f_code.co_name

        self.previous_result.append(result)
        self.previous_operation.append(operation)
        self.previous_input.append(input)

    def get_history(self):
        """
        Get history of this calculator operation.

        """
        if len(self.previous_result) == 0:
            return None

        dict_map = {"add": "+", "multiply": "*"}

        for i in range(len(self.previous_result)):
            print(
                f"{i} ::\t{self.previous_input[i][0]}\t{dict_map[self.previous_operation[i]]}\t{self.previous_input[i][1]}\t=\t{self.previous_result[i]}\n"
            )

