''' Simple calculus game.

    To win, you must enter the correct value
    of random arithmetic expression.
'''
from operator import add, sub, mul
from random import randint, choice


description = 'What is the result of the expression?'


def quest():
    ''' Generate random mathematical expression

        Returns:
            str: Mathematical expression.
    '''
    random_num1 = randint(0, 20)
    random_num2 = randint(0, 20)
    operator = choice('-*+')
    question = f'{random_num1} {operator} {random_num2}'
    return question


def check(question):
    ''' Generate correct answer, that will be
        later compared with player's answer.

        Args:
            question (str): Random mathematic expression.

        Returns:
            value (str): Correct value of the expression.
    '''
    # parse question string
    num1, operator, num2 = [int(elem) if elem not in '-*+'
                            else elem for elem in question.split()]
    if operator == '+':
        value = str(add(num1, num2))
    elif operator == '-':
        value = str(sub(num1, num2))
    elif operator == '*':
        value = str(mul(num1, num2))
    return value
