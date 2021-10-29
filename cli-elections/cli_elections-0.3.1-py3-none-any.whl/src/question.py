from typing import List

import inquirer


def get_input(message: str) -> List:
    return [
        inquirer.Text('question', message=message),
    ]


def get_select(message: str, choices: List = None) -> List:
    return [
        inquirer.List('question', message=message, choices=choices)
    ]
