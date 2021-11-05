import os
import logging
import sys

from pathlib import Path

import click
import docker

from alira_licensing.license import verify as verify_license

from posixpath import split
from click.utils import echo
from dateutil import tz


logging.basicConfig(level=logging.INFO)

HELP_TEXT_VOLUME = "Host's folder containing the configuration of the application"
HELP_TEXT_DOCKER = "Custom docker options to start the containers"
HELP_TEXT_PORT = "Starting port number"
HELP_TEXT_FOLDER = "Local folder containing the docker images"
HELP_TEXT_LOCAL = "Whether cloud synchronization will be disabled"

DEFAULT_PORT = 7000
DEFAULT_VOLUME_PATH = Path(os.path.abspath(""))
NETWORK_NAME = "alira"


class CLI(object):
    """Class containing all of the command line interface commands. """

    def __init__(self, license_data, descriptors, client, volume):
        self.descriptors = descriptors
        self.client = client
        self.volume = volume
        self.github_user = license_data["metadata"]["GITHUB_REPOSITORY_ACCESS_USER"]
        self.github_token = license_data["metadata"]["GITHUB_REPOSITORY_ACCESS_TOKEN"]
        self.not_valid_after = license_data["not_valid_after"]

        self.installed = True
        for descriptor in self.descriptors.values():
            if not descriptor["image"]:
                self.installed = False

    def status(self):
        """Displays the status of the installation."""

        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        utc = self.not_valid_after.replace(tzinfo=from_zone)
        local_datetime = utc.astimezone(to_zone)

        click.echo("License valid until ", nl=False)
        click.secho(f"{local_datetime.strftime('%b %d, %Y')}\n", fg="cyan")

        for descriptor in self.descriptors.values():
            if descriptor["image"]:
                click.echo(f"* {descriptor['name']} {descriptor['version']}", nl=False)
                ports = self._container_ports(descriptor)

                if len(ports) > 0:
                    click.secho(
                        f" (running on {self._format_ports(ports)})", fg="green"
                    )
                else:
                    click.secho(" (not running)", fg="yellow")

            else:
                click.echo(f"* {descriptor['name']}", nl=False)
                click.secho(" (not installed)", fg="cyan")

        click.echo()

    def setup(self, folder, skip_installation_check=False):
        """Installs the application. """

        if not skip_installation_check and self.installed:
            click.echo("The application is already installed. Use ", nl=False)
            click.secho("alr upgrade ", fg="bright_yellow", nl=False)
            click.echo("to install the latest version.")
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

        try:
            networks = self.client.networks.list(names=[NETWORK_NAME])

            if len(networks) == 0:
                self.client.networks.create(NETWORK_NAME, driver="bridge")
        except docker.errors.APIError as exception:
            logging.exception(exception)
            click.echo(f"Unexpected error ocurred when creating network {NETWORK_NAME}")

    def upgrade(self, folder):
        """Upgrades the application. """

        if not self.installed:
            click.echo("The application is not installed. Use ", nl=False)
            click.secho("alr setup ", fg="bright_yellow", nl=False)
            click.echo("to install it.")
            return

        self.remove()
        self.setup(folder, skip_installation_check=True)

    def start(self, local, port, docker_client):
        """Starts the application. """

        if not self.installed:
            click.echo("The application is not installed. Use ", nl=False)
            click.secho("alr setup ", fg="bright_yellow", nl=False)
            click.echo("to install it.")
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
                for params in docker_client
                if params.startswith(f"{descriptor['name']} ")
            ]

            redis_params = list(filter(lambda p: "-e REDIS=" in p, docker_params))

            if len(docker_params) > 0 and len(redis_params) == 0 and not local:
                docker_params[0] += " -e REDIS=redis://redis:6379/1"

            self._start_container(descriptor, local, ports_mapping, docker_params)

    def stop(self):
        """Stops the application. """

        for container in self._running_containers():
            click.echo(f"Stopping {container['descriptor']['name']}...")
            try:
                container["container"].stop()
            except docker.errors.APIError as exception:
                logging.exception(exception)
                click.echo(
                    f"Unexpected error occurred when stopping {container['descriptor']['name']}"
                )

    def restart(self, local, port, docker_client):
        """Restarts the application. """

        self.stop()
        self.start(local, port, docker_client)

    def remove(self):
        """Removes the application. """

        self.stop()

        for descriptor in self.descriptors.values():
            click.echo(f"Removing {descriptor['name']}...")
            self._remove_container(descriptor, remove_image=True)

        try:
            network = self.client.networks.get(NETWORK_NAME)
            network.remove()
        except docker.errors.NotFound:
            pass
        except docker.errors.APIError as exception:
            logging.exception(exception)
            click.echo(f"Unexpected error ocurred when removing network {NETWORK_NAME}")

    def _start_container(self, descriptor, local, ports_mapping, docker_params):
        ports = self._container_ports(descriptor)
        if len(ports) > 0:
            click.echo(
                f"{descriptor['name']} is already running on {self._format_ports(ports)}"
            )
            return

        self._remove_container(descriptor)

        click.echo(f"Starting {descriptor['name']}...")

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
                f"--network-alias {descriptor['name']}",
            ]

            for package_volume in descriptor["volumes"]:
                params.extend(["-v", f"{package_volume[0]}:{package_volume[1]}"])

            params.extend(
                [
                    *ports,
                    *" ".join(docker_params).split(" "),
                    "--rm",
                    descriptor["registry"],
                ]
            )

            try:
                print(" ".join(params))
                result = os.system(" ".join(params))
                print(result)
            except Exception as e:
                logging.exception(e)
                click.echo(f"Unexpected error occurred starting {descriptor['name']}")
        else:
            try:
                volumes = dict()
                for package_volume in descriptor["volumes"]:
                    volumes[package_volume[0]] = {
                        "bind": package_volume[1],
                        "mode": "rw",
                    }

                self.client.containers.run(
                    name=descriptor["name"],
                    image=descriptor["registry"],
                    detach=True,
                    remove=False,
                    restart_policy={"Name": "always"},
                    # volumes={
                    #     descriptor["volume"]: {"bind": "/opt/ml/model", "mode": "rw"}
                    # },
                    volumes=volumes,
                    ports=ports_mapping,
                    environment=["REDIS=redis://redis:6379/1"] if not local else [],
                )
            except docker.errors.APIError as exception:
                logging.exception(exception)
                click.echo(f"Unexpected error occurred starting {descriptor['name']}")

            try:
                networks = self.client.networks.list(names=[NETWORK_NAME])
                if len(networks) > 0:
                    network = networks[0]
                    network.connect(descriptor["name"], aliases=[descriptor["name"]])
            except docker.errors.APIError as exception:
                # This exception is expected if the container is already connected
                # to the network.
                pass

        ports = self._container_ports(descriptor)
        if len(ports) > 0:
            click.echo(
                f"Successfully started {descriptor['name']} using {self._format_ports(ports)}"
            )
        else:
            click.echo(f"Successfully started {descriptor['name']}")

    def _remove_container(self, descriptor, remove_image=False):
        try:
            container = self.client.containers.get(descriptor["name"])
            container.remove()
        except docker.errors.NotFound:
            pass
        except docker.errors.APIError as exception:
            logging.exception(exception)
            click.echo(
                f"Unexpected error ocurred when removing container {descriptor['name']}"
            )

        if remove_image and descriptor["image"]:
            try:
                self.client.images.remove(
                    CLI._registry(descriptor["image"]), force=True
                )
            except docker.errors.APIError as exception:
                logging.exception(exception)
                click.echo(
                    f"Unexpected error ocurred when removing image {descriptor['name']}"
                )

        try:
            networks = self.client.networks.list(names=[NETWORK_NAME])
            if len(networks) > 0:
                network = networks[0]
                network.disconnect(descriptor["name"], force=True)
        except docker.errors.APIError as exception:
            # This exception is expected if the container is already disconnected
            # from the network.
            pass

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
            except docker.errors.APIError as exception:
                logging.exception(exception)
                click.echo(
                    f"Unexpected error occurred downloading {descriptor['name']}"
                )

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
            except docker.errors.APIError as exception:
                logging.exception(exception)
                click.echo(f"Unexpected error occurred loading {descriptor['name']}")

    def _login(self, user, token):
        try:
            result = self.client.login(
                username=user, password=token, registry="ghcr.io"
            )

            return ("Status" in result and result["Status"] == "Login Succeeded") or (
                result["username"] == user and result["password"] == token
            )
        except docker.errors.APIError as exception:
            logging.exception(exception)
            click.echo("Unexpected error occurred when attempting to login")

    @staticmethod
    def initialize(client, volume):
        license_data = CLI._verify(volume)

        descriptors = {}

        for item in license_data["metadata"]["PACKAGES"]:
            package_name = item["name"]
            model = item.get("model", None)

            package_volumes = []

            if "volumes" not in item:
                # The license doesn't specify the volumes that we want to map, so we
                # need to set up the default ones.
                if model:
                    # If this package is a model, we need to map the model-specific folder
                    # to /opt/ml/model.
                    package_volumes.append(
                        (os.path.join(volume, model), "/opt/ml/model")
                    )
                else:
                    # If this package is not a model, we need to map the $volume folder
                    # to /opt/ml/model.
                    package_volumes.append((volume, "/opt/ml/model"))
            else:
                volume_descriptor = item["volumes"]
                volume_mappings = volume_descriptor.split(",")
                for volume_mapping in volume_mappings:
                    volume_mapping = volume_mapping.strip()
                    host, container = volume_mapping.split(":")

                    # If the host path uses the $volume variable, we need to replace it
                    # with the actual volume path.
                    if "$volume" in host:
                        host = host.replace("$volume", volume)

                    # If the host path uses the $model variable, we need to replace it
                    # with the actual model-specific path.
                    if "$model" in host:
                        host = host.replace("$model", os.path.join(volume, model))

                    package_volumes.append((host, container))

            descriptors[item["image"]] = {
                "package": item,
                "name": package_name,
                "volumes": package_volumes,
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

        return CLI(license_data, descriptors, client, volume)

    @staticmethod
    def _verify(volume):
        if not os.path.isfile(os.path.join(volume, "license.pem")):
            click.echo(
                "license.pem file not found. You can either copy the license.pem "
                "file in the current directory, or specify its location using the "
                "--volume argument."
            )
            sys.exit(1)

        if not os.path.isfile(os.path.join(volume, "public_key")):
            click.echo(
                "public_key file not found. You can either copy the public_key "
                "file in the current directory, or specify its location using the "
                "--volume argument."
            )
            sys.exit(1)

        return verify_license(directory=volume)

    @staticmethod
    def _registry(package):
        if "RepoTags" in package.attrs and len(package.attrs["RepoTags"]):
            return package.attrs["RepoTags"][0]

        return package.attrs["Config"]["Image"]


@click.group()
@click.option(
    "--volume",
    "-v",
    help=HELP_TEXT_VOLUME,
    envvar="ALIRA_VOLUME",
    default=DEFAULT_VOLUME_PATH,
)
@click.pass_context
def cli(ctx, volume):
    ctx.ensure_object(dict)

    try:
        docker_client = docker.from_env()
        ctx.obj["CLI"] = CLI.initialize(client=docker_client, volume=volume)
    except docker.errors.APIError as exception:
        logging.exception(exception)
        click.echo("There was an error trying to access the Docker service.")
        click.secho(exception, err=True, fg="red")
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
    ctx.obj["CLI"].start(local, port, docker_client=docker)


@cli.command()
@click.option("--local/--no-local", help=HELP_TEXT_LOCAL, default=False)
@click.option("--port", "-p", help=HELP_TEXT_PORT, default=DEFAULT_PORT)
@click.option("--docker", "-d", multiple=True, help=HELP_TEXT_DOCKER, default=[])
@click.pass_context
def restart(ctx, local, port, docker):
    """Restart the application packages."""
    ctx.obj["CLI"].restart(local, port, docker_client=docker)


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
