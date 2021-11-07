import docker


def container_exists(name, containers=None, client=None):
    """
    check exists in docker container list.

    :param name:
    :param containers:
    :param client:
    :return:
    """

    if containers is None:

        if client is None:
            # create docker client
            client = docker.from_env()

        # get docker networks
        containers = client.containers.list()

    for _container in containers:
        if _container.name == name:
            return True

    return False

# EOF
