import pygame
from .bar import Bar

def bubble_sort(bars):
    """
    A simple bubble sort generator that sorts a single value
    of the array per iteration.

    Parameters
    ----------
    bars : List[Bar]
        A list of Bar objects to be sorted by height

    Returns
    -------
    is_sorted : bool
        Has the array been sorted?
    """

    unsorted_until_index = len(bars) - 1
    is_sorted = False
    step = 1

    while not is_sorted:
        is_sorted = True

        for i in range(unsorted_until_index):
            if bars[i].rect.height > bars[i + 1].rect.height:
                bars[i], bars[i + 1] = bars[i + 1], bars[i]
                is_sorted = False
                yield is_sorted, step
                step += 1

        unsorted_until_index -= 1

    yield is_sorted, step

def selection_sort(bars):
    """
    A simple selection sort generator that sorts a single value
    of the array per iteration.

    Parameters
    ----------
    bars : List[Bar]
        A list of Bar objects to be sorted by height

    Returns
    -------
    is_sorted : bool
        Has the array been sorted?
    """

    is_sorted = False
    step = 1

    for i in range(len(bars) - 1):
        lowest_num_index = i

        for j in range(i, len(bars)):
            if bars[j].rect.height < bars[lowest_num_index].rect.height:
                lowest_num_index = j

        if lowest_num_index != i:
            bars[i], bars[lowest_num_index] = bars[lowest_num_index], bars[i]
            yield is_sorted, step
            step += 1

    is_sorted = True
    yield is_sorted, step

def insertion_sort(bars):
    """
    A simple insertion sort generator that sorts a single value
    of the array per iterations.

    Parameters
    ----------
    bars : List[Bar]
        A list of Bar objects to be sorted by height

    Returns
    -------
    is_sorted : bool
        Has the array been sorted?
    """

    surf = pygame.Surface((8, 0))
    gap = Bar(surf, surf.get_rect())
    is_sorted = False
    step = 1

    for index in range(1, len(bars)):

        temp = bars[index]
        position = index - 1

        while position >= 0:
            if bars[position].rect.height > temp.rect.height:
                bars[position + 1], bars[position] = bars[position], gap
                position -= 1
                yield is_sorted, step,
                step += 1
            else:
                break

        bars[position + 1] = temp

    is_sorted = True
    yield is_sorted, step
