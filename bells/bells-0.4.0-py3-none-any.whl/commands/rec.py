"Recording command"
from datetime import datetime
import logging
import pathlib

import click
import questionary

from ..recording import recorder
from ..linker import FilePath

from .. import utils
from ..colors import style


# TODO: Move validation functions to a separate module
def is_valid_name(name):
    "Checks whether the name is a valid name"
    logging.info("Validating name")
    return "/" not in name and "-" not in name


def is_valid_path(config, path):
    "Checks whether the path is valid"
    logging.info("Validating path")
    return config.root / "structural" in path.resolve().parents


class AllowedNames(click.ParamType):
    "Allowed Names Validator"
    name = "string"

    def convert(self, value, param, ctx):
        if not is_valid_name(value):
            self.fail("Cannot contain / or -")
        return value


def prompt_for_path(config):
    "Interactive prompt to select a path"
    structural = config.root / "structural"

    path = pathlib.Path(".").resolve()
    if structural not in path.parents:
        path = structural
    while True:
        choices = ["."]
        if path != structural:
            choices += [".."]
        choices += [str(i.relative_to(structural)) for i in path.iterdir()
                    if i.is_dir()]
        logging.debug("path=%s choices=%s", path, choices)
        relative_path = str(path.relative_to(structural))
        if relative_path == ".":
            relative_path = ""
        choice = questionary.select("structural/" + relative_path,
                                    choices=choices, style=style,
                                    qmark="").unsafe_ask()
        if choice == ".":
            return path
        if choice == "..":
            path = path.parent
        else:
            path = structural / pathlib.Path(choice)


def prompt_for_name(config, path):
    "Interactive prompt to choose a name"
    logging.debug("Prompting for name")
    logging.debug("Path: %s", path)
    structural = config.root / "structural"
    path = path.relative_to(structural)
    choices = []
    if str(path) in config.autocomplete:
        choices = config.autocomplete[str(path)]
    if choices:
        question = questionary.autocomplete("Choose a name", choices,
                                            style=style, qmark="",
                                            validate=is_valid_name)
    else:
        question = questionary.text("Choose a name", style=style, qmark="",
                                    validate=is_valid_name)
    name = question.unsafe_ask()
    if name not in choices:
        config.autocomplete[str(path)] = [*choices, name]
    return name


@click.command()
@click.argument(
    "path",
    type=click.Path(exists=True, file_okay=False, path_type=pathlib.Path),
    required=False
)
@click.argument("name", required=False, type=AllowedNames())
@utils.require_project
def rec(config, path, name):
    """Records an audio file NAME at PATH

    Prompts for PATH and NAME if they aren't provided.
    """
    if path is None:
        logging.info("No path received as parameter.")
        try:
            path = prompt_for_path(config)
        except KeyboardInterrupt:
            return 1

    if name is None:
        logging.info("No name received as parameter.")
        try:
            name = prompt_for_name(config, path)
        except KeyboardInterrupt:
            return 1

    logging.info("Name: %s", name)
    logging.info("Path: %s", path)
    if not is_valid_name(name) or not is_valid_path(config, path):
        logging.error("Invalid name or path")
        return 2

    now = datetime.now().strftime("%F")
    file = FilePath(config, path, now, name)
    recorder.interactive_recorder(file.path)
    file.link()
    click.echo(f"Finished recording at {file.path}")
    click.echo(f"Finished recording at {file.linked_path}")
    return 0
