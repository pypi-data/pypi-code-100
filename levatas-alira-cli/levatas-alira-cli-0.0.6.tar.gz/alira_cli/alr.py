import os
import click
import docker
import logging
import sys

from posixpath import split
from click.utils import echo
from dateutil import tz
from pathlib import Path
from alira_licensing import license

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HELP_TEXT_VOLUME = "Host's folder containing the configuration of the application"
HELP_TEXT_DOCKER = "Custom docker options to start the containers"
HELP_TEXT_PORT = "Starting port number"
HELP_TEXT_FOLDER = "Local folder containing the docker images"
HELP_TEXT_LOCAL = "Whether cloud synchronization will be disabled"

DEFAULT_PORT = 7000
DEFAULT_VOLUME_PATH = Path(os.path.abspath(""))
NETWORK_NAME = "alira"


class CLI(object):
    def __init__(self, license, descriptors, client, volume):
        self.descriptors = descriptors
        self.client = client
        self.volume = volume
        self.github_user = license["metadata"]["GITHUB_REPOSITORY_ACCESS_USER"]
        self.github_token = license["metadata"]["GITHUB_REPOSITORY_ACCESS_TOKEN"]
        self.not_valid_after = license["not_valid_after"]

        self._installed = True
        for descriptor in self.descriptors.values():
            if not descriptor["image"]:
                self._installed = False

    def installed(self):
        return self._installed

    def status(self):
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        utc = self.not_valid_after.replace(tzinfo=from_zone)
        local_datetime = utc.astimezone(to_zone)

        click.echo(f"License valid until {local_datetime.strftime('%b %d, %Y')}.")

        for descriptor in self.descriptors.values():
            if descriptor["image"]:
                click.echo(f"* {descriptor['name']} {descriptor['version']}", nl=False)
                ports = self._container_ports(descriptor)

                if len(ports) > 0:
                    click.secho(
                        f" (running on {self._format_ports(ports)})", fg="green"
                    )
                else:
                    click.echo(f" (not running)")

            else:
                click.echo(f"* {descriptor['name']}", nl=False)
                click.secho(f" (not installed)", fg="yellow")

    def setup(self, folder, skip_installation_check=False):
        if not skip_installation_check and self.installed():
            click.echo(
                "The application is already installed. Use `alr upgrade` to upgrade it to the latest version."
            )
            return

        if folder is None:
            if self._login(
                user=self.github_user,
                token=self.github_token,
            ):
                self._download()
            else:
                click.echo("An error ocurred while login into docker.")
        else:
            self._load(folder)

        networks = self.client.networks.list(names=[NETWORK_NAME])

        if len(networks) == 0:
            self.client.networks.create(NETWORK_NAME, driver="bridge")

    def upgrade(self, folder):
        if not self.installed():
            click.echo(
                "The application is not currently installed. Use `alr setup` to install the available packages."
            )
            return

        self.remove()
        self.setup(folder, skip_installation_check=True)

    def start(self, local, port, docker):
        if not self.installed():
            click.echo(
                "The application is not currently installed. Use `alr setup` to install the available packages."
            )
            return

        port_number = port
        for descriptor in self.descriptors.values():

            ports_mapping = {}
            if descriptor["binding"]:
                for port in descriptor["ports"]:
                    ports_mapping[port] = port_number
                    port_number += 1

            docker_params = [
                params[len(f"{descriptor['name']} ") :]
                for params in docker
                if params.startswith(f"{descriptor['name']} ")
            ]

            redis_params = list(filter(lambda p: "-e REDIS=" in p, docker_params))

            if len(docker_params) and not len(redis_params) and not local:
                docker_params[0] += " -e REDIS=redis://redis:6379/1"

            self._start_container(descriptor, local, ports_mapping, docker_params)

    def stop(self):
        for container in self._running_containers():
            try:
                click.echo(f"Stopping {container['descriptor']['name']}...")
                container["container"].stop()
            except Exception as e:
                logger.exception(e)
                click.echo(
                    f"Unexpected error occurred when stopping {container['descriptor']['name']}"
                )

    def restart(self, local, port, docker):
        self.stop()
        self.start(local, port, docker)

    def remove(self):
        self.stop()

        for descriptor in self.descriptors.values():
            if descriptor["image"]:
                try:
                    click.echo(f"Removing {descriptor['name']}...")
                    self.client.images.remove(
                        CLI._registry(descriptor["image"]), force=True
                    )
                except Exception as e:
                    logger.exception(e)
                    click.echo(
                        f"Unexpected error ocurred when removing {descriptor['name']}..."
                    )

    def _start_container(self, descriptor, local, ports_mapping, docker_params):
        ports = self._container_ports(descriptor)
        if len(ports) > 0:
            click.echo(
                f"{descriptor['name']} is already running on {self._format_ports(ports)}"
            )
            return

        click.echo(f"Starting {descriptor['name']}...")

        try:
            if len(docker_params):
                ports = (
                    [
                        f"-p {external}:{internal.split('/')[0]}"
                        for internal, external in ports_mapping.items()
                    ]
                    if ports_mapping is not None
                    else []
                )
                params = [
                    "docker",
                    "container",
                    "run",
                    "-it",
                    "--detach",
                    "--name",
                    descriptor["name"],
                    f"--network {NETWORK_NAME}",
                    "-v",
                    f"{descriptor['volume']}:/opt/ml/model",
                    *ports,
                    *" ".join(docker_params).split(" "),
                    "--rm",
                    descriptor["registry"],
                ]

                print(" ".join(params))
                result = os.system(" ".join(params))
                print(result)
            else:
                self.client.containers.run(
                    name=descriptor["name"],
                    image=descriptor["registry"],
                    network=NETWORK_NAME,
                    detach=True,
                    remove=False,
                    restart_policy={"Name": "always"},
                    volumes={
                        descriptor["volume"]: {"bind": "/opt/ml/model", "mode": "rw"}
                    },
                    ports=ports_mapping,
                    environment=["REDIS=redis://redis:6379/1"] if not local else [],
                )

            ports = self._container_ports(descriptor)
            if len(ports) > 0:
                click.echo(
                    f"Successfully started {descriptor['name']} using {self._format_ports(ports)}"
                )
            else:
                click.echo(f"Successfully started {descriptor['name']}")
        except Exception as e:
            logger.exception(e)
            click.echo(f"Unexpected error occurred starting {descriptor['name']}")

    def _container_ports(self, descriptor):
        ports = []

        containers = self._running_containers({descriptor["registry"]: descriptor})
        container = containers[0] if containers else None

        if container:
            if descriptor["binding"]:
                port_bindings = container["container"].attrs["HostConfig"][
                    "PortBindings"
                ]
                for binding_key in port_bindings:
                    for binding in port_bindings[binding_key]:
                        ports.append(int(binding["HostPort"]))
            else:
                for port in (
                    container["container"].attrs["NetworkSettings"]["Ports"].keys()
                ):
                    ports.append(int(port.replace("/tcp", "")))

        return ports

    def _running_containers(self, descriptors=None):
        if not descriptors:
            descriptors = self.descriptors

        containers = []
        for container in self.client.containers.list():
            registry_image_name = CLI._registry(container)
            if registry_image_name in descriptors:
                containers.append(
                    {
                        "descriptor": descriptors[registry_image_name],
                        "container": container,
                    }
                )

        return containers

    def _format_ports(self, ports):
        if len(ports) == 1:
            return f"port {ports[0]}"

        return "ports " + ", ".join([str(p) for p in ports])

    def _download(self):
        for descriptor_image, descriptor in self.descriptors.items():
            click.echo(f"Downloading {descriptor['name']}...")

            try:
                for line in self.client.api.pull(
                    descriptor_image, stream=True, decode=True
                ):
                    if "progress" in line:
                        message = f"{line['status']} - {line['progress']}"
                    elif "status" in line:
                        message = line["status"]
                    elif "errorDetail" in line:
                        message = line["errorDetail"].get("message", "Error")
                        click.echo(message)
                        sys.exit(1)

                    print(message, end="\r")

                click.echo("")

                click.echo(f"{descriptor['name']} successfully downloaded")
            except Exception as e:
                logger.exception(e)
                click.echo(f"Package {descriptor['name']} download failed.")

    def _load(self, folder):
        if not os.path.exists(folder):
            click.echo(f"The specified folder {folder} does not exist.")
            return

        for descriptor in self.descriptors.values():
            image_file = os.path.join(folder, f"{descriptor['name']}.tar.gz")

            try:
                with open(image_file, mode="rb") as file:
                    click.echo(
                        f"Loading {descriptor['name']} from file '{image_file}'..."
                    )
                    self.client.images.load(file.read())
                    click.echo(f"{descriptor['name']} successfully loaded.")
            except Exception as e:
                logger.exception(e)
                click.echo(
                    f"Unexpected error ocurred trying to load {descriptor['name']} image."
                )

    def _login(self, user, token):
        try:
            result = self.client.login(
                username=user, password=token, registry="ghcr.io"
            )

            return ("Status" in result and result["Status"] == "Login Succeeded") or (
                result["username"] == user and result["password"] == token
            )
        except Exception as e:
            logger.exception(e)
            return False

    @staticmethod
    def initialize(client, volume):
        license = CLI._verify(volume)

        descriptors = {}

        for item in license["metadata"]["PACKAGES"]:
            package_name = item["name"]
            model = item.get("model", None)
            package_volume = os.path.join(volume, model) if model else volume

            descriptors[item["image"]] = {
                "package": item,
                "name": package_name,
                "volume": package_volume,
                "registry": item["image"],
                "image": None,
                "binding": item.get("binding", False),
            }

        if client and client.images:
            for container_image in client.images.list():
                registry_image_name = CLI._registry(container_image)
                if registry_image_name in descriptors:
                    descriptors[registry_image_name]["image"] = container_image

                    index = descriptors[registry_image_name]["registry"].rindex(":")
                    version = descriptors[registry_image_name]["registry"][index + 1 :]

                    if container_image.attrs["Config"]["Labels"]:
                        version = container_image.attrs["Config"]["Labels"].get(
                            "org.opencontainers.image.version", None
                        )

                        if version:
                            version = version.replace("v", "")

                    descriptors[registry_image_name]["version"] = version

                    if descriptors[registry_image_name]["binding"]:
                        exposed_ports = (
                            container_image.attrs["Config"]["ExposedPorts"]
                            if "ExposedPorts" in container_image.attrs["Config"]
                            else {}
                        )

                        descriptors[registry_image_name]["ports"] = [
                            port for port in exposed_ports
                        ]

        return CLI(license, descriptors, client, volume)

    @staticmethod
    def _verify(volume):
        if not os.path.isfile(os.path.join(volume, "license.pem")):
            click.echo(
                "license.pem file not found. You can either copy the license.pem file in the current directory, or specify its location using the --volume argument."
            )
            sys.exit(1)

        if not os.path.isfile(os.path.join(volume, "public_key")):
            click.echo(
                "public_key file not found. You can either copy the public_key file in the current directory, or specify its location using the --volume argument."
            )
            sys.exit(1)

        return license.verify(directory=volume)

    @staticmethod
    def _registry(package):
        if "RepoTags" in package.attrs and len(package.attrs["RepoTags"]):
            return package.attrs["RepoTags"][0]

        return package.attrs["Config"]["Image"]


@click.group()
@click.option("--volume", "-v", help=HELP_TEXT_VOLUME, default=DEFAULT_VOLUME_PATH)
@click.pass_context
def cli(ctx, volume):
    ctx.ensure_object(dict)

    try:
        docker_client = docker.from_env()
        ctx.obj["CLI"] = CLI.initialize(client=docker_client, volume=volume)
    except Exception as e:
        click.echo("There was an error trying to access the Docker service.")
        click.secho(e, err=True, fg="red")
        sys.exit(1)


@cli.command()
@click.pass_context
def status(ctx):
    """Display license and version information of each package."""
    ctx.obj["CLI"].status()


@cli.command()
@click.option("--folder", "-f", help=HELP_TEXT_FOLDER, default=None)
@click.pass_context
def setup(ctx, folder):
    """Install the application."""
    ctx.obj["CLI"].setup(folder)


@cli.command()
@click.option("--folder", "-f", help=HELP_TEXT_FOLDER, default=None)
@click.pass_context
def upgrade(ctx, folder):
    """Upgrade the application packages to their latest version."""
    ctx.obj["CLI"].upgrade(folder)


@cli.command()
@click.option("--local/--no-local", help=HELP_TEXT_LOCAL, default=False)
@click.option("--port", "-p", help=HELP_TEXT_PORT, default=DEFAULT_PORT)
@click.option("--docker", "-d", multiple=True, help=HELP_TEXT_DOCKER, default=[])
@click.pass_context
def start(ctx, local, port, docker):
    """Start the application packages."""
    ctx.obj["CLI"].start(local, port, docker)


@cli.command()
@click.option("--local/--no-local", help=HELP_TEXT_LOCAL, default=False)
@click.option("--port", "-p", help=HELP_TEXT_PORT, default=DEFAULT_PORT)
@click.option("--docker", "-d", multiple=True, help=HELP_TEXT_DOCKER, default=[])
@click.pass_context
def restart(ctx, local, port, docker):
    """Restart the application packages."""
    ctx.obj["CLI"].restart(local, port, docker)


@cli.command()
@click.pass_context
def stop(ctx):
    """Stop the application packages."""
    ctx.obj["CLI"].stop()


def remove_cancelled_callback(ctx, param, value):
    if not value:
        click.echo("The remove operation was cancelled.")
        sys.exit(1)


@cli.command()
@click.option(
    "--yes",
    is_flag=True,
    callback=remove_cancelled_callback,
    expose_value=False,
    prompt="Are you sure you want to remove the installed packages?",
)
@click.pass_context
def remove(ctx):
    """Remove the application packages."""
    ctx.obj["CLI"].remove()


@cli.command()
@click.argument("subcommand", required=False)
@click.pass_context
def help(ctx, subcommand=None):
    subcommand_obj = cli.get_command(ctx, subcommand)
    if subcommand_obj is None:
        click.echo(cli.get_help(ctx))
    else:
        click.echo(subcommand_obj.get_help(ctx))
