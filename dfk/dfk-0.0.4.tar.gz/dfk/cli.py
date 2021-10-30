import os
import sys

import click

CONTEXT_SETTINGS = dict(auto_envvar_prefix="dfk")

cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "commands"))


class DfkCli(click.MultiCommand):
    api_instance = None

    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith(".py") and filename.startswith("cmd_"):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode("ascii", "replace")
            mod = __import__(
                "dfk.commands.cmd_{}".format(name), None, None, ["cli"]
            )
        except ImportError:
            return
        return mod.cli


@click.command(cls=DfkCli, context_settings=CONTEXT_SETTINGS)
def cli():
    """🐳 dfk - Write once, run away!"""
