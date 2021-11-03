"""CLI 'delete' command and subcommands"""

import click
from matatika.cli.utility import Resolver
from matatika.types import Resource
from .root import matatika


@matatika.group('delete', short_help='Delete resources')
@click.pass_context
@click.option("--bypass-confirm", is_flag=True, help="Bypass delete confirmation")
def delete(ctx, bypass_confirm):
    """Delete resources"""

    ctx.obj['bypass_confirm'] = bypass_confirm


@delete.command('workspaces', short_help='Delete workspaces')
@click.pass_context
@click.argument("workspace-ids", type=click.UUID, nargs=-1, required=True)
def delete_workspace(ctx, workspace_ids):
    """Delete workspaces"""

    client = Resolver(ctx).client(workspace_id=None)

    delete_confirmed = ctx.obj['bypass_confirm']

    if not delete_confirmed:
        confirmation_message = "This action cannot be undone. Do you want to continue? [y/N]"

        delete_confirmed = click.confirm(
            text=_warning(confirmation_message),
            prompt_suffix=_warning(": "),
            show_default=False)

    if delete_confirmed:
        client.delete_resources(Resource.WORKSPACE, *workspace_ids)
        click.secho("Successfully deleted workspace(s): " +
                    ", ".join(str(w) for w in workspace_ids), fg='green')


@ delete.command('datasets', short_help='Delete datasets')
@ click.pass_context
@ click.argument("dataset-ids", type=click.UUID, nargs=-1, required=True)
def delete_dataset(ctx, dataset_ids):
    """Delete datasets"""

    client = Resolver(ctx).client(workspace_id=None)

    delete_confirmed = ctx.obj['bypass_confirm']

    if not delete_confirmed:
        confirmation_message = "This action cannot be undone. Do you want to continue? [y/N]"

        delete_confirmed = click.confirm(
            text=_warning(confirmation_message),
            prompt_suffix=_warning(": "),
            show_default=False)

    if delete_confirmed:
        client.delete_resources(Resource.DATASET, *dataset_ids)
        click.secho("Successfully deleted dataset(s): " +
                    ", ".join(str(d) for d in dataset_ids), fg='green')


def _warning(text: str) -> str:

    return click.style(text, fg='yellow')
