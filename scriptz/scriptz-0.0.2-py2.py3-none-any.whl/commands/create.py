import os
import subprocess
import string
from pathlib import Path
from typer import Argument

from rich.prompt import Prompt

from scriptz import cli, Manager


@cli.command()
def new(folder_path: Path = Argument(None)):
    """ Create a new script. """
    manager = Manager()
    folder = manager.get_folder(folder_path)

    file_type = Prompt.ask(
        "File Type",
        choices=manager.config.file_types,
        default=manager.config.default_type,
    )
    handler = manager.config.get_handler(file_type)

    description = Prompt.ask("Description")

    file_name = make_file_name(description, manager.config.file_length)
    new_script = folder.create_script(file_name, handler.suffix)

    # initialize default content
    contents = [f"{handler.comment} {description}"]
    if handler.comment == "#":
        contents.insert(0, f"#!/usr/bin/env {handler.command}")
    new_script.path.write_text("\n".join(contents))

    editor = os.getenv("EDITOR", "vim")
    subprocess.call("%s %s" % (editor, new_script.path), shell=True)


def make_file_name(text: str, max_length: int = 20) -> str:
    max_length = max(max_length, 6)  # at least 6 characters
    text = text.lower()
    text = "".join(ch if ch in lower_alphanum else " " for ch in text)
    words = text.split()

    if len("_".join(words)) > max_length:
        filtered_words = list(word for word in words if word not in stop_words)
        if filtered_words:
            words = filtered_words

    trim = None
    text = "_".join(words[:trim])
    while len(text) > max_length:
        trim = (trim - 1) if trim is not None else -1
        text = "_".join(words[:trim])

    return text


lower_alphanum = set(string.ascii_lowercase + string.digits)

stop_words = {
    "a",
    "and",
    "as",
    "at",
    "but",
    "by",
    "for",
    "from",
    "i",
    "in",
    "it",
    "not",
    "of",
    "on",
    "or",
    "s",
    "t",
    "that",
    "the",
    "this",
    "to",
    "up",
    "with",
    "you",
}
