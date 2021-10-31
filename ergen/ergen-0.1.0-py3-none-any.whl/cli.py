import typer
import yaml
import types
from . import main
from . import types

app = typer.Typer()


@app.command()
def ping(
    input_file: str = typer.Argument(..., help="Input file"),
):
    """
    Ping pong
    """
    typer.echo(f"Input file: {input_file}")

    with open(input_file, "r") as f:
        data = yaml.safe_load(f)
        typer.echo(yaml.dump(data))


@app.command()
def er(
    input_file: str = typer.Argument(..., help="Input file"),
):
    """
    Entity-Relation document
    """
    with open(input_file, "r") as f:
        data = yaml.safe_load(f)
        main.main(types.ErdType(**data))


@app.callback()
def callback():
    pass


if __name__ == "__main__":
    app()
