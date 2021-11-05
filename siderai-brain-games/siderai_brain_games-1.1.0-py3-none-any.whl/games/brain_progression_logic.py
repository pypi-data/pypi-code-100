''' Arithmetic progression game.

    To win, you must find the missing element of progression.
    (The most complicated game of the package in terms of code).
'''
from random import randint


description = ('What number is missing in the progression?')


def quest():
    ''' Generate random arithmetic progression
        with 10 elems and one of them randomly missing.

        Returns:
            progression_as_string (str)
    '''
    # generate variables for creating the progression
    start_number = randint(0, 30)
    step = randint(0, 20)
    missing_index = randint(0, 9)
    # create list of progression's elements
    sample_ints = elems_listing(start_number, step)
    # convert elements into string format
    sample = [str(x) for x in sample_ints]
    # hide the value
    sample[missing_index] = '..'
    # convert progression into string with one missing element
    progression_as_string = ' '.join(sample)
    return progression_as_string


def check(progression):
    ''' Generate correct answer, that will be
        later compared with player's answer.

        Args:
            progression (str): Question line with one element missing.

        Returns:
            value (str): Missing element.
    '''
    # prog as str > prog as list,
    # convert num elements from str into ints
    prog = [int(x) if x != '..' else x for x in progression.split()]
    # calculate the missing element
    value = str(find_missing(prog))
    return value


def elems_listing(start, step):
    ''' Progression generator.

        Args:
            start (int): First number of progression;
            step (int): Step of progression.

        Returns:
            progression (list): 10 elems.
    '''
    progression = [start]
    i = 1
    while i <= 9:
        current = progression[i - 1] + step
        progression.append(current)
        i += 1
    return progression


def find_missing(lizt):
    ''' Progression decryptor.

        Args:
            lizt (list): Progression with one missing elem.

        Returns:
            The value of missing element (int).
    '''
    index = lizt.index('..')  # only one is missing, so the method is secure
    if index == 0:
        return lizt[1] - (lizt[2] - lizt[1])
    if index == 9:
        return lizt[8] + (lizt[8] - lizt[7])
    else:
        return (lizt[index - 1] + lizt[index + 1]) // 2
