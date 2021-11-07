import click
from canalyse.parser import ConductivityParser
from canalyse.validator import ConductivityValidator


def get_validator(filename):
    parser = ConductivityParser()
    df = parser.run(filename)
    validator = ConductivityValidator(df)
    return validator


@click.group()
def cli():
    pass


@cli.command()
@click.option("--grater-than", type=float)
@click.option("--less-than", type=float)
@click.option("--quantity", type=click.Choice(["std", "average", "variance"]))
@click.argument("filename", type=click.File("rb"))
def conductivity(grater_than, less_than, quantity, filename):
    validator = get_validator(filename)
    if quantity == "std":
        if grater_than is not None:
            if validator.standard_deviation_is_more_than(grater_than):
                return
            else:
                click.echo(
                    f"Standard deviation of {filename} is less than {grater_than}."
                )
        else:
            if validator.standard_deviation_is_less_than(less_than):
                return
            else:
                click.echo(
                    f"Standard deviation of {filename} is grater than {less_than}."
                )
    elif quantity == "average":
        if grater_than is not None:
            if validator.average_is_more_than(grater_than):
                return
            else:
                click.echo(f"Average of {filename} is less than {grater_than}.")
        else:
            if validator.average_is_less_than(less_than):
                return
            else:
                click.echo(f"Average of {filename} is grater than {less_than}.")
    elif quantity == "variance":
        if grater_than is not None:
            if validator.variance_is_more_than(grater_than):
                return
            else:
                click.echo(f"Variance of {filename} is less than {grater_than}.")
        else:
            if validator.variance_is_less_than(less_than):
                return
            else:
                click.echo(f"Variance of {filename} is grater than {less_than}.")


@cli.command()
def current():
    click.echo("Current calculation is not supported now.")


if __name__ == "__main__":
    cli()
