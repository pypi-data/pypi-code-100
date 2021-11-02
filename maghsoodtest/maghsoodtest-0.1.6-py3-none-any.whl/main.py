def odd(start, stop):
    for x in range(start, stop + 1, 2):
        yield x


def print_odd_number(start, stop):
    return list(odd(start, stop))