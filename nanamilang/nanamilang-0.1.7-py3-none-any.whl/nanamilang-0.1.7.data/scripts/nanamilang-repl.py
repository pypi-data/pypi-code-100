#!python

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

"""NanamiLang REPL"""

import os
import atexit
import readline
import argparse
from typing import List, Any
from nanamilang import Program
from nanamilang import datatypes
from nanamilang.builtin import Library, Help
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
    keywords: List[str] = ['help', 'exit']
    builtins: List[str] = list(Library.library.keys())
    vocabulary = keywords + builtins
    results: List[Any] = [x for x in vocabulary if x.startswith(t)] + [None]
    return results[s]


readline.set_completer(complete)


def main():
    """NanamiLang REPL Main function"""

    parser = argparse.ArgumentParser('NanamiLang REPL')
    parser.add_argument('--dumptree',
                        help='Dump tree each time',
                        action='store_true', default=False)

    args = parser.parse_args()

    print('NanamiLang', __version_string__, 'by', __author__, '(Python 3)')
    print('Type :help to get help')
    print('Type :exit to exit the REPL')
    # print('History have been read and will be appended to', history_file_path)

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
            finally:
                # TODO: implement try-except-finally correctly!!
                if res is not None:
                    if res.name == datatypes.Keyword.name:
                        if res.reference() == 'help':
                            print(Help.help())
                            continue
                        elif res.reference() == 'exit':
                            print('Such an elegant way to exit')
                            break
                    print(res.format())
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
