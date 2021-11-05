#!/usr/bin/env python3.

import prompt
from brain_games import cli


def is_even():
    name = cli.name
    count = 0
    while count < 3:
        random_number = cli.random_num()
        print('Question: ' + str(random_number))
        user_answer = prompt.string('Your Answer: ')
        correct = ''
        if random_number % 2 == 0 and user_answer == 'yes':
            cli.correct_answer()
            count = count + 1
        elif random_number % 2 != 0 and user_answer == 'no':
            cli.correct_answer()
            count = count + 1
        elif random_number % 2 == 0:
            correct = 'yes'
            cli.wrong_answer(user_answer, correct, name)
            return
        elif random_number % 2 != 0:
            correct = 'no'
            cli.wrong_answer(user_answer, correct, name)
            return
        else:
            cli.wrong_answer(user_answer, correct, name)
            return
    cli.congrats(name)
