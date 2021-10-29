import os

def build_table(table):
    col_widths = [0] * len(table)

    for y in range(len(table)):
        for x in table[y]:
            if col_widths[y] < len(x):
                col_widths[y] = len(x)

    resp = ""
    for x in range(len(table[0])):
        for y in range(len(table)):
            resp += table[y][x].ljust(col_widths[y]) + ' '
        resp += "\n"
    return resp


def random_bytes(length):
    rand_bytes = os.urandom(length)
    return rand_bytes


def bytes_to_string(bytearray):
    resp = "[{}".format(bytearray[0])
    for index in range(1, len(bytearray)):
        resp += " {}".format(bytearray[index])
    resp += "]"
    return resp