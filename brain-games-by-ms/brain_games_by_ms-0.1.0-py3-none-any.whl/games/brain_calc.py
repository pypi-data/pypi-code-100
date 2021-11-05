#!/usr/bin/env python3.


import operator
from random import choice

import prompt
from brain_games import cli


ops = {'+': operator.add, '-': operator.sub, '*': operator.mul}


def calc():
    name = cli.name
    count = 0
    while count < 3:
        num_one = cli.random_num()
        num_two = cli.random_num()
        expression = choice(list(ops.keys()))
        correct = (ops[expression](num_one, num_two))
        print('Question: ' + str(num_one) + expression + str(num_two))
        user_answer = prompt.string('Your Answer: ')
        if user_answer == str(correct):
            cli.correct_answer()
            count = count + 1
        else:
            cli.wrong_answer(user_answer, correct, name)
            return
    cli.congrats(name)
