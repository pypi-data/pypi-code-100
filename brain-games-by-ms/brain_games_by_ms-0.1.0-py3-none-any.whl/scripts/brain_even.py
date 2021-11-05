#!/usr/bin/env python3.

from brain_games.cli import is_even_question, welcome_user
from brain_games.games.brain_even import is_even


def main():
    welcome_user()
    is_even_question()
    is_even()


if __name__ == '__main__':
    main()
