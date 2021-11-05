from enum import Enum
from pathlib import Path

import typer
from tabulate import tabulate

from .api import create_api
from .commons import parse_csv, parse_json, parse_jsonlines
from .exceptions import cli_wrapper

app = typer.Typer()
token_app = typer.Typer(help="Manage API Tokens.")
app.add_typer(token_app, name="token")


@app.command("create")
@cli_wrapper
def create_bucket(
    description: str = typer.Option("", show_default=False),
    schemaless: bool = typer.Option(
        False,
        "--schemaless",
        help="Create a schemaless bucket.",
        show_default=False,
    ),
):
    """
    Create a new bucket.
    """
    api = create_api()
    payload = api.Buckets.create(description, schemaless=schemaless)
    typer.echo(
        typer.style(
            "Bucket created, you can start sending data 🚀",
            fg=typer.colors.WHITE,
            bold=True,
        )
    )
    first_row = ("uuid", "name", "description", "url")
    values = [getattr(payload, entry) for entry in first_row]
    first_row = ("ID", "Name", "Description", "URL")
    typer.echo(
        tabulate(
            [first_row, values], headers="firstrow", tablefmt="fancy_grid"
        )
    )


@app.command("list")
@cli_wrapper
def list_buckets():
    """
    Get a list of your buckets.
    """
    api = create_api()
    payload = api.Buckets.list()
    first_row = ("uuid", "name", "description", "url")

    if not payload:
        typer.echo(
            typer.style(
                "Ohhhh... no buckets :)", fg=typer.colors.MAGENTA, bold=True
            )
        )
        return

    rows = []
    for index, row in enumerate(payload, 1):
        rows.append([index, *[getattr(row, entry) for entry in first_row]])

    first_row = ("ID", "Name", "Description", "URL", "Schemaless")
    first_row = ("", *first_row)
    typer.echo(
        tabulate([first_row, *rows], headers="firstrow", tablefmt="fancy_grid")
    )


@app.command("delete")
@cli_wrapper
def delete_bucket(bucket: str):
    """
    Delete a bucket.
    """
    api = create_api()
    api.Buckets.delete(bucket)
    typer.echo(
        typer.style(
            f"Bucket {bucket} deleted.", fg=typer.colors.WHITE, bold=True
        )
    )


@app.command("query")
@cli_wrapper
def query_bucket(query: str = typer.Argument(...)):
    """
    Query a bucket using a SQL query.
    """
    api = create_api()
    payload = api.Buckets.query(query)
    for row in payload:
        typer.echo(row)


@token_app.command("create")
@cli_wrapper
def create_token(
    bucket: str = typer.Argument(
        ..., help="The bucket uuid you want to give access to."
    ),
    description: str = typer.Option(""),
):
    """
    Create a new API Token.
    """
    api = create_api()
    client = api.Bucket(bucket)
    payload = client.create_token(description)
    typer.echo(
        typer.style(
            "Bucket Token created.",
            fg=typer.colors.WHITE,
            bold=True,
        )
    )
    typer.echo(
        typer.style(
            "⚠️  PLEASE SAVE THE TOKEN, THIS IS THE ONLY TIME WHERE WE DISPLAY IT ⚠️",
            fg=typer.colors.WHITE,
            bold=True,
        )
    )
    first_row = ("uuid", "token", "description", "created_on")
    values = [payload[entry] for entry in first_row]
    first_row = ("ID", "Token", "Description", "Created on")
    typer.echo(
        tabulate(
            [first_row, values], headers="firstrow", tablefmt="fancy_grid"
        )
    )


@token_app.command("list")
@cli_wrapper
def list_tokens(bucket: str = typer.Argument(..., help="The bucket uuid.")):
    """
    Get your tokens.
    """
    api = create_api()
    client = api.Bucket(bucket)
    tokens = client.get_tokens()
    first_row = ("uuid", "token", "description", "created_on")
    if not tokens:
        typer.echo(
            typer.style(
                f"No tokens for Bucket({bucket}).",
                fg=typer.colors.WHITE,
                bold=True,
            )
        )
        return

    rows = []
    for index, row in enumerate(tokens, 1):
        rows.append([index, *[row[entry] for entry in first_row]])

    first_row = ("ID", "Token", "Description", "Created on")
    first_row = ("", *first_row)
    typer.echo(
        tabulate([first_row, *rows], headers="firstrow", tablefmt="fancy_grid")
    )


@token_app.command("delete")
@cli_wrapper
def delete_token(bucket_uuid: str, token_uuid: str):
    """
    Delete an API Token.
    """
    api = create_api()
    client = api.Bucket(bucket_uuid)
    client.delete_token(token_uuid=token_uuid)
    typer.echo(
        typer.style(
            f"Bucket Token {token_uuid} deleted.",
            fg=typer.colors.WHITE,
            bold=True,
        )
    )


class DataFileFormat(str, Enum):
    csv = "csv"
    json = "json"
    jsonlines = "jsonlines"


@app.command("push")
@cli_wrapper
def push_data(
    bucket_uuid: str,
    file: Path = typer.Option(
        ...,
        help="The path to the data file",
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
    ),
    format: DataFileFormat = typer.Option(
        ..., help="The format of the data file", case_sensitive=False
    ),
):
    """
    Push the content of a data file into the bucket.
    The file can be CSV, JSON, or JSON-lines.
    """
    if format == DataFileFormat.csv:
        rows = parse_csv(file)
    elif format == DataFileFormat.json:
        rows = parse_json(file)
    elif format == DataFileFormat.csv:
        rows = parse_jsonlines(file)

    api = create_api()
    bucket = api.Bucket(bucket_uuid)
    bucket.push_data(rows=rows)
    typer.echo(
        typer.style(
            "The data has been loaded 🚀.",
            fg=typer.colors.WHITE,
            bold=True,
        )
    )
