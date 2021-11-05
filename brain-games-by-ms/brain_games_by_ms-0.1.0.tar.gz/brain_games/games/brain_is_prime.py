#!/usr/bin/env python3.

import prompt
from brain_games import cli


def is_prime_logic(num):
    i = 2
    if num < 2:
        return False
    elif i >= 2:
        while i <= num / 2:
            if num % i == 0:
                return False
            i += 1
        return True


def is_prime():
    name = cli.name
    count = 0
    while count < 3:
        number = cli.random_num()
        if is_prime_logic(number) is True:
            correct = 'yes'
        else:
            correct = 'no'
        print('Question: ' + str(number))
        user_answer = prompt.string('Your Answer: ')
        if user_answer == correct:
            cli.correct_answer()
            count = count + 1
        else:
            cli.wrong_answer(user_answer, correct, name)
            return
    cli.congrats(name)
