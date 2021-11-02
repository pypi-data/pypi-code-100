from . import context
from .input_helpers import get_org_from_input_or_ctx
from .output.table import (
    format_table,
    metadata_column,
    spec_column,
    column,
    subtable,
)
import agilicus


def get(ctx, id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs.pop("org_id", None)
    return apiclient.launchers_api.get_launcher(id, org_id=org_id, **kwargs)


def delete(ctx, id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs.pop("org_id", None)
    return apiclient.launchers_api.delete_launcher(id, org_id=org_id, **kwargs)


def add(ctx, resource_members=[], **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs.pop("org_id", None)

    spec = agilicus.LauncherSpec(org_id=org_id, **kwargs)

    member_objs = []
    for member in resource_members:
        member_objs.append(agilicus.ResourceMember(id=member))
    launcher = agilicus.Launcher(spec=spec, resource_members=member_objs)
    return apiclient.launchers_api.create_launcher(launcher)


def query(ctx, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)

    kwargs["org_id"] = org_id
    query_results = apiclient.launchers_api.list_launchers(**kwargs)
    return query_results.launchers


def replace(
    ctx,
    id,
    resource_members=None,
    remove_resource_members=None,
    name=None,
    org_id=None,
    command_path=None,
    command_arguments=None,
    start_in=None,
    **kwargs,
):
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    resource = apiclient.launchers_api.get_launcher(id, org_id=org_id)
    if remove_resource_members is not None:
        old_members = resource.spec.resource_members
        resource.spec.resource_members = []
        for member in old_members:
            if member.id in remove_resource_members:
                # needs to be removed.
                continue
            resource.spec.resource_members.append(member)

    if resource_members is not None:
        for member in resource_members:
            resource.spec.resource_members.append(agilicus.ResourceMember(id=member))
    if name is not None:
        resource.spec.name = name
    if resource.spec.config is None:
        resource.spec.config = agilicus.LauncherConfig()
    if command_path is not None:
        resource.spec.config.command_path = command_path
    if command_arguments is not None:
        resource.spec.config.command_arguments = command_arguments
    if start_in is not None:
        resource.spec.config.start_in = start_in
    return apiclient.launchers_api.replace_launcher(id, launcher=resource).to_dict()


def format_launchers(ctx, launchers):
    app_service_columns = [
        column("id"),
        column("name"),
    ]
    fs_columns = [
        metadata_column("id"),
        spec_column("name"),
    ]
    columns = [
        metadata_column("id"),
        spec_column("org_id", "org id"),
        spec_column("name", "name"),
        spec_column("config", "config"),
        subtable(ctx, "status.file_shares", fs_columns, optional=True),
        subtable(ctx, "status.application_services", app_service_columns, optional=True),
    ]
    return format_table(ctx, launchers, columns)
