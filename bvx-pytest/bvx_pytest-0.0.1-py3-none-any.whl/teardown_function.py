import docker


def teardown_function():
    # create docker client
    _client = docker.from_env()

    # get docker networks
    _networks = _client.networks.list()

    # prune docker network for pytest
    _client.networks.prune()


if __name__ == "__main__":
    # execute only if run as a script
    teardown_function()

# EOF
