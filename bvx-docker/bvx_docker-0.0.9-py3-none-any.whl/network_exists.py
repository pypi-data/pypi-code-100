import docker


def network_exists(name, networks=None, client=None):
    """
    check exists in docker network list.

    :param name:
    :param networks:
    :param client:
    :return:
    """

    if networks is None:

        if client is None:
            # create docker client
            client = docker.from_env()

        # get docker networks
        networks = client.networks.list()

    for _network in networks:
        if _network.name == name:
            return True

    return False

# EOF
