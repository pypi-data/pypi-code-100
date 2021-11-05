#!/usr/bin/env python3.

from brain_games.cli import welcome_user, progression_question
from brain_games.games.brain_progression import progression


def main():
    welcome_user()
    progression_question()
    progression()


if __name__ == '__main__':
    main()
