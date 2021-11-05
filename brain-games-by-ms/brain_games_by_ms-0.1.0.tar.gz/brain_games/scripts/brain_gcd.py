#!/usr/bin/env python3.

from brain_games.cli import welcome_user, gcd_question
from brain_games.games.brain_gcd import gcd_func


def main():
    welcome_user()
    gcd_question()
    gcd_func()


if __name__ == '__main__':
    main()
