import json
from json.decoder import JSONDecodeError

import click
from defektor_api.exceptions import ApiException

import dfk.config
from dfk.cli import DfkCli


@click.group("plan")
def cli():
    """📜 Fault injection plans."""


@dfk.config.require_login
@cli.command()
@click.argument("id", required=True)
def get(id):
    """Print plan details."""

    try:
        get_plan_result = DfkCli.api_instance.plan_get(plan_id=id)
        click.echo(get_plan_result)
    except ApiException as api_exception:
        click.echo(f"ERROR: retrieving the plan for id {id}.\n{api_exception}")


@dfk.config.require_login
@cli.command()
def list():
    """Lists running, stopped, and completed plans."""

    try:
        list_plans_result = DfkCli.api_instance.plan_list()
        click.echo(list_plans_result)
    except ApiException as api_exception:
        click.echo(f"ERROR: retrieving plans list.\n{api_exception}")


@dfk.config.require_login
@cli.command()
@click.argument("file", type=click.Path(exists=True))
def start(file):
    """Starts a new plan described in a JSON file."""

    try:
        with open(file, 'r') as plan_file:
            json_plan_data = plan_file.read()

        plan_obj = json.loads(json_plan_data)

        start_plan_result = DfkCli.api_instance.plan_add(plan=plan_obj)
        click.echo(start_plan_result)
    except ApiException as api_exception:
        click.echo(f"ERROR: starting the new plan.\n{api_exception}")
    except IOError as read_file_exception:
        click.echo(f"ERROR: reading plan file.\n{read_file_exception}")
    except JSONDecodeError as json_exception:
        click.echo(f"ERROR: reading json file.\n{json_exception}")


@dfk.config.require_login
@cli.command()
@click.argument("id", required=True)
def stop(id):
    """Stops a running plan."""

    try:
        stop_plan_result = DfkCli.api_instance.plan_delete(plan_id=id)
        click.echo(stop_plan_result)
    except ApiException as api_exception:
        click.echo(f"ERROR: stopping the plan.\n{api_exception}")


@dfk.config.require_login
@cli.command()
@click.argument("file", type=click.Path(exists=True))
def validate(file_path):
    """Validates a given JSON file with the plan configuration."""

    try:
        with open(file_path, 'r') as plan_file:
            plan_data = plan_file.read()

        plan_obj = json.loads(plan_data)

        validate_plan_result = DfkCli.api_instance.plan_validate(plan=plan_obj)
        click.echo(validate_plan_result)
    except ApiException as api_exception:
        click.echo(f"ERROR: validating the plan.\n{api_exception}")
    except IOError as read_file_exception:
        click.echo(f"ERROR: reading plan file.\n{read_file_exception}")
    except JSONDecodeError as json_exception:
        click.echo(f"ERROR: reading json file.\n{json_exception}")


@dfk.config.require_login
@cli.command()
def template():
    """Generates a template file for a plan."""

    # TODO: We don't have a schema to generate a plan template.
    raise NotImplementedError("You must implement the template() method yourself!")
