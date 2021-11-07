# coding: utf-8
"""Main entrypoint of cli."""
from inspect import getmembers, isfunction

import click
from tableaudocumentapi import Workbook

from tabassist.check import CheckField
from tabassist.error import ErrorRegistry


@click.group()
def cli():
    """Command line tool for working with Tableau workbook faster."""
    pass


@click.command()
@click.option('--file', '-f',
              required=True,
              help='Tableau filepath for check.')
@click.option('--summary', '-s',
              is_flag=True,
              help='Show errors statistic for current checking.')
def check(file, summary):
    """Check given Tableau workbook for errors."""
    wb = Workbook(file)

    errors = ErrorRegistry()

    for source in wb.datasources:
        for field in source.fields:
            for e in CheckField(source.fields[field]).run():
                if e:
                    errors.add(e)
    if summary:
        errors.show_summary()
    else:
        errors.show_errors()


cli.add_command(check)

if __name__ == '__main__':
    cli()
