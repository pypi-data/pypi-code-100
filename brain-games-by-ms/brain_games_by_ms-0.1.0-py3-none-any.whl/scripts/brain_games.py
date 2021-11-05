#!/usr/bin/env python3.

import prompt
from brain_games.cli import is_even_question, welcome_user, calc_question, gcd_question, progression_question, is_prime_rule
from brain_games.games.brain_calc import calc
from brain_games.games.brain_gcd import gcd_func
from brain_games.games.brain_even import is_even
from brain_games.games.brain_progression import progression
from brain_games.games.brain_is_prime import is_prime


def main():
    welcome_user()
    list = {1: 'is_even', 2: 'calc', 3: 'gcd', 4: 'progression', 5: 'is_prime'}
    print('Choose a game ' + str(list))
    user_answer = prompt.string('Your choice: ')
    if user_answer == '1':
        is_even_question()
        is_even()
    elif user_answer == '2':
        calc_question()
        calc()
    elif user_answer == '3':
        gcd_question()
        gcd_func()
    elif user_answer == '4':
        progression_question()
        progression()
    elif user_answer == '5':
        is_prime_rule()
        is_prime()
    else:
        print('Wrong game index. Try again!')


if __name__ == '__main__':
    main()
