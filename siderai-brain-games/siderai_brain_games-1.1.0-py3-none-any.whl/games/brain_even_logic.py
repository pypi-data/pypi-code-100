''' Prime numbers game.

    To win, you must define whether
    given number is prime or not.
'''

from random import randint


description = 'Answer "yes" if the number is even, otherwise answer "no".'


def quest():
    ''' Generate random number. '''
    quest_number = randint(0, 99999)
    return quest_number


def check(quest_number):
    ''' Test if given number is prime.

        Args:
            quest_number (int): Random number in range 99999.

        Returns:
            value (str): Test output ('yes' / 'no').
    '''
    if quest_number % 2 == 0:
        value = 'yes'
    else:
        value = 'no'
    return value
