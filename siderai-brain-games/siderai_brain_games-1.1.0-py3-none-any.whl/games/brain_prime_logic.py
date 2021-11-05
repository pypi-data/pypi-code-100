''' Prime number game.

    To win, you must define whether
    a random number is prime or not.
'''
from random import randint


description = 'Answer "yes" if given number is prime. Otherwise answer "no".'


def quest():
    number = randint(0, 200)
    return number


def check(number):
    return is_prime(number)


def is_prime(num):
    if num <= 1:
        return 'no'
    for i in range(2, int(num / 2) + 1):
        if (num % i) == 0:
            return 'no'
    return 'yes'
