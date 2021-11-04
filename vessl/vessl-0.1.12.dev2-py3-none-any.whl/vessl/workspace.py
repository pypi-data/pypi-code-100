import os
import urllib.parse
from pathlib import Path
from typing import List
from zipfile import ZipFile

import click
import inquirer
import paramiko

from openapi_client.models import ResponseWorkspaceDetail, ResponseWorkspaceList
from vessl import vessl_api
from vessl.organization import _get_organization_name
from vessl.util.common import parse_time_to_ago
from vessl.util.config import VesslConfigLoader
from vessl.util.constant import (
    SSH_CONFIG_FORMAT,
    SSH_CONFIG_PATH,
    WORKSPACE_TEMP_ZIP_PATH,
    WORKSPACE_ZIP_PATH,
)
from vessl.util.exception import InvalidWorkspaceError
from vessl.util.zipper import Zipper
from vessl.volume import copy_volume_file


def read_workspace(workspace_id: int, **kwargs) -> ResponseWorkspaceDetail:
    """Read workspace

    Keyword args:
        organization_name (str): override default organization
    """
    return vessl_api.workspace_read_api(
        workspace_id=workspace_id, organization_name=_get_organization_name(**kwargs)
    )


def list_workspaces(
    cluster_id: int = None, statuses: List[str] = None, mine: bool = True, **kwargs
) -> List[ResponseWorkspaceList]:
    """List workspaces

    Keyword args:
        organization_name (str): override default organization
    """
    return vessl_api.workspace_list_api(
        organization_name=_get_organization_name(**kwargs),
        cluster=cluster_id,
        mine=mine,
        statuses=statuses,
    ).results


def backup_workspace() -> None:
    """Backup the home directory of the workspace

    Should only be called inside a workspace.
    """

    workspace_id = VesslConfigLoader().workspace
    if workspace_id is None:
        raise InvalidWorkspaceError("Can only be called within a workspace.")

    workspace = read_workspace(workspace_id)

    zipper = Zipper(WORKSPACE_TEMP_ZIP_PATH, "w")
    zipper.zipdir(str(Path.home()), zipper)
    zipper.close()

    copy_volume_file(
        source_volume_id=None,
        source_path=zipper.filename,
        dest_volume_id=workspace.backup_volume_id,
        dest_path=os.path.basename(zipper.filename),
    )

    vessl_api.cli_workspace_backup_api(workspace_id=workspace_id)


def restore_workspace() -> None:
    """Restore the home directory from the previous backup

    Should only be called inside a workspace.
    """

    workspace_id = VesslConfigLoader().workspace
    if workspace_id is None:
        raise InvalidWorkspaceError("Can only be called within a workspace.")

    workspace_list = list_workspaces(mine=True)
    backup_workspaces = [w for w in workspace_list if w.last_backup_dt is not None]
    if len(backup_workspaces) == 0:
        raise click.ClickException("Available workspace backup not found.")

    workspace = inquirer.prompt(
        [
            inquirer.List(
                "question",
                message="Select workspace",
                choices=[
                    (
                        f"{w.name} (backup created {parse_time_to_ago(w.last_backup_dt)})",
                        w,
                    )
                    for w in backup_workspaces
                ],
            )
        ],
        raise_keyboard_interrupt=True,
    ).get("question")

    copy_volume_file(
        source_volume_id=workspace.backup_volume_id,
        source_path=WORKSPACE_ZIP_PATH,
        dest_volume_id=None,
        dest_path=WORKSPACE_TEMP_ZIP_PATH,
    )

    z = ZipFile(WORKSPACE_TEMP_ZIP_PATH)
    z.extractall(str(Path.home()))


def connect_workspace_ssh(private_key_path: str, **kwargs) -> None:
    """Connect to a running workspace via SSH

    Keyword args:
        organization_name (str): override default organization
    """
    running_workspaces = list_workspaces(statuses=["running"], mine=True)
    if len(running_workspaces) == 0:
        raise click.ClickException("There is no running workspace.")

    if len(running_workspaces) == 1:
        workspace = running_workspaces[0]
    else:
        workspace = inquirer.prompt(
            [
                inquirer.List(
                    "question",
                    message="Select workspace",
                    choices=[
                        (f"{w.name} (created {parse_time_to_ago(w.created_dt)})", w)
                        for w in running_workspaces
                    ],
                )
            ],
            raise_keyboard_interrupt=True,
        ).get("question")

    ssh_endpoint = urllib.parse.urlparse(workspace.endpoints.ssh.endpoint)
    ssh_private_key_option = f" -i {private_key_path}" if private_key_path else ""
    os.system(
        f"ssh -p {ssh_endpoint.port}{ssh_private_key_option} vessl@{ssh_endpoint.hostname}"
    )


def update_vscode_remote_ssh(private_key_path: str) -> None:
    """Update .ssh/config file for VSCode Remote-SSH plugin"""
    running_workspaces = list_workspaces(statuses=["running"], mine=True)
    if len(running_workspaces) == 0:
        raise click.ClickException("There is no running workspace.")

    ssh_config = paramiko.SSHConfig()
    try:
        with open(SSH_CONFIG_PATH, "r") as fr:
            ssh_config.parse(fr)
    except FileNotFoundError:
        pass

    host_set = ssh_config.get_hostnames()
    for workspace in running_workspaces:
        host = f"{workspace.name}-{int(workspace.created_dt.timestamp())}"
        if host in host_set:
            continue

        ssh_endpoint = urllib.parse.urlparse(workspace.endpoints.ssh.endpoint)

        config_value = SSH_CONFIG_FORMAT.format(
            host=host,
            hostname=ssh_endpoint.hostname,
            port=ssh_endpoint.port,
        )
        if private_key_path:
            config_value += f"    IdentityFile {private_key_path}\n"

        with open(SSH_CONFIG_PATH, "a") as f:
            f.write(config_value)
