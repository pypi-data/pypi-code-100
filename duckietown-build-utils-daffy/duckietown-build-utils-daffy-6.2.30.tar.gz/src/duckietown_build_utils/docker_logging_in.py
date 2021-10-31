from typing import Set, Tuple

import docker
from zuper_commons.types import ZException

from . import logger
from .buildresult import parse_complete_tag
from .credentials import DockerCredentials
from .types import DockerCompleteImageName, DockerRegistryName, DockerSecret, DockerUsername

__all__ = ["DockerLoginError", "docker_login", "do_login_for_registry", "do_login_for_image"]


class DockerLoginError(ZException):
    pass


class LoggedInStorage:
    done: Set[Tuple[DockerRegistryName, DockerUsername]] = set()


def docker_login(
    client: docker.DockerClient,
    registry: DockerRegistryName,
    docker_username: DockerUsername,
    docker_password: DockerSecret,
):
    k = registry, docker_username
    if k in LoggedInStorage.done:
        pass
        # logger.debug(f"Already logged as {docker_username!r} to {registry}")
        # logger.warn(f'we will do it again {docker_password!r}')
    LoggedInStorage.done.add(k)
    # client = docker.from_env()
    res = client.login(username=docker_username, password=docker_password, reauth=True, registry=registry)
    # logger.info("client login", res=res)
    return
    #
    # cmd = ["docker", "login", "-u", docker_username, "--password-stdin", registry]
    # try:
    #     res = subprocess.check_output(cmd, input=docker_password.encode(), stderr=subprocess.PIPE)
    # except subprocess.CalledProcessError as e:
    #     stderr = e.stderr.decode() if e.stderr else "Not captured"
    #     stdout = e.stdout.decode() if e.stdout else "Not captured"
    #     is_timeout = "Client.Timeout" in stderr
    #     if is_timeout:
    #         msg = f"Docker timeout while logging in."
    #         raise DockerLoginError(msg, e=e.stderr.decode()) from None
    #
    #     n = len(docker_password)
    #
    #     password_masked = docker_password[0] + "*" * (n - 2) + docker_password[-1]
    #     msg = f'Failed to login with username "{docker_username}".'
    #     msg += f" password is {password_masked}"
    #     raise DockerLoginError(msg, cmd=e.cmd, returncode=e.returncode, stdout=stdout, stderr=stderr) from e
    # logger.debug(f"docker login to {registry} username {docker_username} OK res = {res}")


def do_login_for_image(
    client: docker.DockerClient, credentials: DockerCredentials, im: DockerCompleteImageName
):
    if im is None:
        raise ValueError("im is None")
    try:
        br = parse_complete_tag(im)
        do_login_for_registry(client, credentials, br.registry)
    except Exception as e:
        msg = f"Could not log in for image {im!r}"
        raise Exception(msg) from e


def do_login_for_registry(
    client: docker.DockerClient, credentials: DockerCredentials, registry: DockerRegistryName
):
    if registry is None:
        raise ValueError("registry is None")
    if registry in credentials:
        docker_login(client, registry, credentials[registry]["username"], credentials[registry]["secret"])
    else:
        logger.warn(f"No credentials to login to registry {registry!r}", known=list(credentials))
