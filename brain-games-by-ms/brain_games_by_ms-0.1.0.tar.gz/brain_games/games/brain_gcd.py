#!/usr/bin/env python3.

import prompt
from brain_games import cli


def gcd(num_one, num_two):
    if num_two == 0:
        return num_one
    return gcd(num_two, num_one % num_two)


def gcd_func():
    name = cli.name
    count = 0
    while count < 3:
        num_one = cli.random_num()
        num_two = cli.random_num()
        correct = gcd(num_one, num_two)
        print('Question: ' + str(num_one) + ' ' + str(num_two))
        user_answer = prompt.string('Your Answer: ')
        if user_answer == str(correct):
            cli.correct_answer()
            count = count + 1
        else:
            cli.wrong_answer(user_answer, correct, name)
            return
    cli.congrats(name)
