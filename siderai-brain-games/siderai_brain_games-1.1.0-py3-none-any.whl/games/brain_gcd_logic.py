''' Greatest common divisitor game.

    To win, you must find gcd for random pair of numbers.
'''
from random import randint
from math import gcd

description = 'Find the greatest common divisor of given numbers.'


def quest():
    '''Generate two random numbers and present them as a string.'''
    number1 = randint(0, 40)
    number2 = randint(0, 40)
    question = f'{number1} {number2}'
    return question


def check(question):
    ''' Generate correct answer, that will be
        later compared with player's answer.

        Args:
            question (str): Random couple of numbers.

        Returns:
            value (str): Correct gcd for the couple.
    '''
    # parse question string
    number1, number2 = [int(elem) for elem in question.split()]
    value = str(gcd(number1, number2))
    return value
