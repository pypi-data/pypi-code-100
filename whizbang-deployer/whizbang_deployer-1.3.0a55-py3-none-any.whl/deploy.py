from whizbang.__main__ import execute


def deploy(solution_type, solution_directory, env_config_file_name: str = "env_config.json", client_config_file_name: str = None):

    if ".json" not in env_config_file_name:
        env_config_file_name += ".json"

    if client_config_file_name is not None and ".json" not in client_config_file_name:
        client_config_file_name += ".json"

    execute(solution_type, solution_directory, env_config_file_name, client_config_file_name)