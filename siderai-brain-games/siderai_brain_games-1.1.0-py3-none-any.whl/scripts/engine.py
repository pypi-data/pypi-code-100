''' This module builds a common pattern for all the games,
    so gameplay is separated from games' content (DRY).

    To win, you must give 3 correct answers in a row,
    otherwise you lose.

    Args:
        desc (str): Description of the game;
        quest (func > int/str): Generate the question;
        check (func > str): Checkout answer for question.
'''
import prompt


def build_and_play(desc, quest, check):
    print('Welcome to the Brain Games!')
    name = prompt.string('May I have your name? ')
    print(f'Hello, {name}!')
    correct_answers = 0
    print(desc)  # arg
    while correct_answers < 3:
        question = quest()  # arg
        correct_value = check(question)  # arg
        answer = input(f'Question: {question}? ')
        if answer == correct_value:
            print('Correct!')
            correct_answers += 1
            continue
        print(f'"{answer}" is wrong answer ;(.',
              f'Correct answer was "{correct_value}"')
        print(f'Let\'s try again, {name}!')  # with any mistake the game ends
        return
    print(f'Congratulations, {name}!')
