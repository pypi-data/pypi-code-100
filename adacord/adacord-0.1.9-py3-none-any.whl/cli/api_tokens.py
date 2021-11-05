import typer
from tabulate import tabulate

from .api import create_api
from .exceptions import cli_wrapper

app = typer.Typer()


@app.command("create")
@cli_wrapper
def create_api_token(
    description: str = typer.Option(""),
):
    """
    Create a new API Token.
    """
    api = create_api()
    payload = api.ApiTokens.create(description)
    typer.echo(
        typer.style(
            "API Token created.",
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


@app.command("list")
@cli_wrapper
def list_api_tokens():
    """
    Get your API tokens.
    """
    api = create_api()
    api_tokens = api.ApiTokens.list()
    first_row = ("uuid", "token", "description", "created_on")
    if not api_tokens:
        typer.echo(
            typer.style(
                "No API tokens.",
                fg=typer.colors.WHITE,
                bold=True,
            )
        )
        return

    rows = []
    for index, row in enumerate(api_tokens, 1):
        rows.append([index, *[row[entry] for entry in first_row]])

    first_row = ("ID", "Token", "Description", "Created on")
    first_row = ("", *first_row)
    typer.echo(
        tabulate([first_row, *rows], headers="firstrow", tablefmt="fancy_grid")
    )


@app.command("delete")
@cli_wrapper
def delete_api_token(token_uuid: str):
    """
    Delete an API Token.
    """
    api = create_api()
    api.ApiTokens.delete(token_uuid=token_uuid)
    typer.echo(
        typer.style(
            f"API Token {token_uuid} deleted.",
            fg=typer.colors.WHITE,
            bold=True,
        )
    )
