#!python

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

"""NanamiLang REPL"""

import os
import sys
import atexit
import readline
import argparse
from typing import List, Any
from nanamilang import Program
from nanamilang import datatypes
from nanamilang.builtin import Builtin, BuiltinMacro
from nanamilang import __version_string__, __author__

history_file_path = os.path.join(
    os.path.expanduser("~"), ".nanamilang_history")
try:
    readline.read_history_file(history_file_path)
    readline.set_history_length(1000)
except FileNotFoundError:
    pass

atexit.register(readline.write_history_file, history_file_path)

readline.parse_and_bind("tab: complete")


def complete(t: str, s: int):
    """NanamiLang REPL complete() function for GNU readline"""
    vocabulary = Builtin.completions() + BuiltinMacro.completions()
    results: List[Any] = [x for x in vocabulary if x.startswith(t)] + [None]
    return results[s]


readline.set_completer(complete)


def main():
    """NanamiLang REPL Main function"""

    parser = argparse.ArgumentParser('NanamiLang REPL')
    parser.add_argument('--no-greeting',
                        help='Greeting can be disabled',
                        action='store_true', default=False)
    parser.add_argument('--dumptree',
                        help='Dump tree each time',
                        action='store_true', default=False)

    args = parser.parse_args()

    p_ver = '.'.join([str(sys.version_info.major),
                      str(sys.version_info.minor),
                      str(sys.version_info.micro)])

    print('NanamiLang', __version_string__, 'by', __author__, 'on Python', p_ver)
    if not args.no_greeting:
        print('Type (doc function-or-macro) to see function-or-macro sample doc')
        print('Type (exit!) or press "Control+D" / "Control+C" to exit the REPL')
        print('History has been read and will be appended to', history_file_path)

    Builtin.install(
        {
            'name': 'exit!', 'type': 'function',
            'sample': '(exit!)', 'docstring': 'Exit NanamiLang REPL'
        },
        lambda _: sys.exit(0)
    )

    while True:
        try:
            inp = input("USER> ")
            # Currently, nor Program nor Tokenizer do not accept empty input lines
            if not inp:
                continue
            res = None
            try:
                p = Program(inp)
                if args.dumptree:
                    p.dump_tree()
                res = p.evaluate()
            except Exception as e:
                res = datatypes.NException.from_python(e)
            if res is not None:
                print(res.format())
            else:
                print(datatypes.Nil('nil').format())
        except EOFError:
            print("Bye for now!")
            break
        except KeyboardInterrupt:
            print("\b\bBye for now!")
            break

    return 0

    # explicitly return 0 to the system as each good program should do (I am a good boi)


if __name__ == "__main__":

    main()
