import typer
from splitn.sequences import random_sequence
from splitn.split import splitted
from loguru import logger
from random import seed

@logger.catch
def generate_output(
        operand: str,
        separator: str,
        as_pattern: bool,
        times: int
    ):
    for counter in range(times):
        sequence = random_sequence(operand) if as_pattern else operand
        for splitted_sequence in splitted(sequence, separator):
            typer.echo(splitted_sequence)
        if counter < times - 1:
            typer.echo()

app = typer.Typer()

@app.command()
def main(operands: list[str] = typer.Argument(
            None,
            help='List of strings to be splitted or regexes describing desired strings (when -p flag is on).'
        ),
        separator: str = typer.Option(
            ' ',
            '--separator', '-s',
            help='Separator used in splitting generated sequences.'
        ),
        as_pattern: bool = typer.Option(
            False,
            '--pattern', '-p',
            help='Treat given operands as regular expressions defining strings to be splitted.'
        ),
        times: int = typer.Option(
            1,
            '--times', '-t',
            help='Number of times splitn generates sequences for each specification.'
        )
    ):
    if not operands:
        raise typer.Exit()
    else:
        operands_counter = range(len(operands), 0, -1)
        for operand, counter in zip(operands, operands_counter):
            try:
                generate_output(operand, separator, as_pattern, times)
                if counter > 1:
                    typer.echo()
            except Exception as e:
                raise typer.Abort('Program aborted with exception: %s.'.format(e))

if __name__ == '__main__':
    app()
