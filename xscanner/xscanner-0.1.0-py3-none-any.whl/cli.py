import os
import sys

import antlr4
import click

from xscanner import __version__, core
from xscanner.modules import anything


@click.group()
@click.version_option(__version__)
def main():
    return 0

def print_result(result):
    print(result[0][0])
    for r in result[0][1]:
        print('  ->', r)
    for item in result[1]:
        print('  *', item[0])
        for i in item[1]:
            print('    ->', i)        


@click.command()
@click.argument("rule")
@click.argument("path")
def scan(rule, path):
    scanner = core.Scanner(rule)


    if os.path.isdir(path):
        for f in os.listdir(path):
            p = os.path.join(path, f)
            result = scanner.scan(p)
            print_result(result)
    elif os.path.isfile(path):
        result = scanner.scan(path)
        print_result(result)


main.add_command(scan)

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
