import json
import os
import signal
import subprocess
import sys

import click

from clio.config import Config
from clio.prerequisites.giove import Giove
from clio.prerequisites.remote_connections_utilities import RemoteConnectionsUtilities
from clio.shell import Shell
from clio.kube.container import Container
from clio.path import Path
from clio.sync import generate_command, sync_options


VERSION = "0.3.6"


@click.group()
@click.version_option(version=VERSION)
def cli():
    pass


def handle_keyboard_interrupt(signal, frame):
    print("\nKeyboardInterrupt has been caught. Cleaning up...")
    return 0


@cli.command(help="Check status of all containers")
def check():
    command = "kubectl get pods"
    result = Shell.run(command).stdout
    click.echo(result)


@cli.command(help="Get the logs of the specified container")
@click.argument("name")
def logs(name):
    Container.check_existence(name)
    command = f"kubectl logs -f deployment/{name} -c {name}"
    signal.signal(signal.SIGINT, handle_keyboard_interrupt)
    try:
        return Shell.run(command, without_stdout=True)
    except KeyboardInterrupt:
        return 0


@cli.command(help="Enter the specified container")
@click.argument("name")
def enter(name):
    Container.check_existence(name)
    command = f"kubectl exec -it deployment/{name} -c {name} -- /bin/sh"
    return Shell.run(command, without_stdout=True)


@cli.command(help="Restart the specified container")
@click.argument("name")
def restart(name):
    Container.check_existence(name)
    container_id = Container.get_id(name)
    command = f"docker container restart {container_id}"
    return Shell.run(command, without_stdout=True)


@cli.group(help="Cleanup development stuff not used anymore")
def cleanup():
    pass


@cleanup.command(help="Cleanup unnecessary docker images & containers")
def docker():
    Shell.run_cleanup_command("image")
    Shell.run_cleanup_command("container")


@cli.command(help="Save your remote SSH credentials for easier use of sync commands")
@click.option("--name")
@click.option("--password")
@click.option("--ip")
def config(name, password, ip):
    config_file = Config.create_file()
    if name is None or password is None or ip is None:
        click.echo("Missing SSH credentials. Please try again.")
        return
    if name == "" or password == "" or ip == "":
        click.echo("SSH credentials cannot be empty. Please try again.")
        return
    credentials = {"name": name, "password": password, "ip": ip}
    json.dump(credentials, config_file)
    subprocess.run([f"sudo sshpass -p {password} ssh {name}@{ip}"], shell=True)


@cli.group(help="Synchronize your code")
def sync():
    pass


@sync.command(help="Sync giove code")
@sync_options
@click.argument("path")
@click.pass_context
def giove(ctx, path, name=None, password=None, ip=None):
    __check_config(ctx, name, password, ip)
    ip, name, password = __get_credentials()
    __check_remote_path_exists(name, ip, password, path)
    if not Giove.are_prerequisites_installed():
        Giove.install_prerequisites()
    command = generate_command(username=name, ip=ip, password=password, path=path, service_name="giove")
    return Shell.run(command)


@sync.command(help="Sync minerva code")
@sync_options
@click.argument("path")
@click.pass_context
def minerva(ctx, path, name=None, password=None, ip=None):
    __check_config(ctx, name, password, ip)
    ip, name, password = __get_credentials()
    __check_remote_path_exists(name, ip, password, path)
    if not RemoteConnectionsUtilities.are_installed("minerva"):
        RemoteConnectionsUtilities.install("minerva")
    command = generate_command(username=name, ip=ip, password=password, path=path, service_name="minerva")
    return Shell.run(command)


@sync.command(help="Sync doorman code")
@sync_options
@click.argument("path")
@click.pass_context
def doorman(ctx, path, name=None, password=None, ip=None):
    __check_config(ctx, name, password, ip)
    ip, name, password = __get_credentials()
    __check_remote_path_exists(name, ip, password, path)
    if not RemoteConnectionsUtilities.are_installed("doorman"):
        RemoteConnectionsUtilities.install("doorman")
    command = generate_command(username=name, ip=ip, password=password, path=path, service_name="doorman/doorman")
    return Shell.run(command)


@sync.command(help="Sync diana code")
@sync_options
@click.argument("path")
@click.pass_context
def diana(ctx, path, name=None, password=None, ip=None):
    __check_config(ctx, name, password, ip)
    ip, name, password = __get_credentials()
    __check_remote_path_exists(name, ip, password, path)
    command = f"sshpass -p {password} rsync -azvh -e ssh {name}@{ip}:{path} /usr/share/syneto-diana"
    return Shell.run(command)


def __check_config(ctx, name=None, password=None, ip=None):
    if not os.path.isfile("./config.json") or os.path.getsize("./config.json") == 0:
        if name is None or password is None or ip is None:
            click.echo("Missing config information. Please enter your correct name, password and IP and try again.")
            sys.exit()
        ctx.invoke(config, name=name, password=password, ip=ip)


def __get_credentials():
    try:
        ip, name, password = Config.get_ssh_credentials()
        return ip, name, password
    except Exception as e:
        click.echo(f"Error encountered while trying to get credentials: {e}")
        sys.exit()


def __check_remote_path_exists(name, ip, password, path):
    if path == "":
        click.echo("Path cannot be empty.")
        sys.exit()
    if not Path.exists_remote(name + "@" + ip, password, path):
        click.echo("The given remote path does not exist. Plase try again.")
        sys.exit()


if __name__ == "__main__":
    cli()
