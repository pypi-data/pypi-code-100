#!/usr/bin/env python3

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

"""NanamiLang Eval"""

import os
import argparse
from nanamilang import Program, datatypes


def main():
    """NanamiLang Eval Main function"""

    parser = argparse.ArgumentParser('NanamiLang Evaluator')
    parser.add_argument('program', help='Path to source code')
    args = parser.parse_args()

    assert args.program
    assert os.path.exists(args.program)

    with open(args.program, encoding='utf-8') as r:
        inp = r.read()

    assert inp, 'A program source code could not be an empty string'

    dt = Program(inp).evaluate()

    print(dt.reference())

    if dt.name == datatypes.IntegerNumber.name:
        return dt.reference()
    return 0

    # return 0 by default, or if the result type is IntegerNumber, return its value


if __name__ == "__main__":

    main()
