#!/usr/bin/env python
from brain_games.scripts.engine import build_and_play
from brain_games.games.brain_progression_logic import description, quest, check


def main():
    build_and_play(description, quest, check)


if __name__ == '__main__':
    main()
