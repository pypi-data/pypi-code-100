"""
Created on Sat Oct 30 19:29:30 2021

@author: siddharthvenkatesh

This is a command line interface for scraper1830.
"""

import click
from .scraper1830 import Scraper1830


@click.group()
def cli_entry():
    pass


@cli_entry.command()
@click.option(
    "--id", prompt="Enter Game ID", help="The id for the 1830 game on 18xx.games"
)
def plot_history(id):
    scraper = Scraper1830(id)
    scraper.plot_player_history()


if __name__ == "__main__":
    cli_entry()
