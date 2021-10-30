"""Main program."""

from typing import List, Sequence

import click

from . import __version__, commands
from .click_ext import OrderedGroup


@click.group(
    cls=OrderedGroup,
    invoke_without_command=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.pass_context
@click.option("--version", is_flag=True, help="Show the version.")
@click.option("--debug/--no-debug", is_flag=True, help="Enable the debugging mode.")
def main(  # noqa: D103  # to suppress the help message
    ctx: click.Context, version: bool, debug: bool
) -> None:
    if ctx.invoked_subcommand is None:
        if version:
            click.echo(f"python-grace {__version__}")
        else:
            click.echo(main.get_help(ctx))
    else:
        ctx.ensure_object(dict)
        ctx.obj["DEBUG"] = debug


def _complete_template_name(
    ctx: click.Context, param: str, incomplete: str
) -> List[str]:
    names = commands.template.list_templates()
    return [k for k in names if k.startswith(incomplete)]


@main.command(no_args_is_help=True)
@click.argument("name", shell_complete=_complete_template_name)
def template(name: str) -> None:
    """Copy a template in.prc to the current directory."""
    commands.template.copy_template(name)


def _add_template_help() -> None:
    if not template.help:
        return

    names = commands.template.list_templates()

    if names:
        s = ", ".join(names)
        template.help += f"\n\nNAME must be one of: {s}."


_add_template_help()


def _add_raw_commands() -> None:
    args = click.Argument(["args"], required=False, nargs=-1)
    context_settings = {"ignore_unknown_options": True, "help_option_names": []}

    def make_callback(c: click.decorators.F) -> click.decorators.F:
        @click.pass_context
        def callback(ctx: click.Context, args: Sequence[str]) -> None:
            c(args, ctx.obj["DEBUG"])

        return callback  # type: ignore[return-value]

    for c in commands.raw_commands.values():
        if not c.available:
            continue
        name = c.name

        cmd = click.Command(
            name,
            context_settings=context_settings,
            callback=make_callback(c),
            params=[args],
            help=f"Run {name}.",
        )
        main.add_command(cmd)


_add_raw_commands()
