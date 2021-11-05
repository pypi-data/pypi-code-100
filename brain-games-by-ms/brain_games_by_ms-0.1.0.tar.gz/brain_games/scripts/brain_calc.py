#!/usr/bin/env python3.

from brain_games.cli import welcome_user, calc_question
from brain_games.games.brain_calc import calc


def main():
    welcome_user()
    calc_question()
    calc()


if __name__ == '__main__':
    main()
