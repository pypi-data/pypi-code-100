import sys

from whizbang.container.application_container import ApplicationContainer
from whizbang.domain.menu.menu_invoker import MenuInvoker

from whizbang.util.json_helpers import import_local_json
from whizbang.util.deployment_helpers import merge_client_config


# see: https://python-dependency-injector.ets-labs.org/examples/decoupled-packages.html
def start_interactive():
    # todo: will need an override
    menu: MenuInvoker = create_container().menu_package.menu_invoker()
    menu.display_menu()


def execute(solution_type, solution_directory, env_config_file_name: str, client_config_file_name: str = None):
    print("executing command line mode")
    container = create_container(solution_directory, env_config_file_name, client_config_file_name)
    solution_factory = container.solution_factory()
    solution = solution_factory.get_solution(solution_type)
    solution.deploy()


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    if len(args) == 0:
        start_interactive()
    elif args[0].upper() == 'RUN':
        execute(args)


def import_and_merge_environment_configs(current_dir_path: str, env_config_file_name: str,
                                         client_config_file_name: str = None):
    default_config_json = import_local_json(f'{current_dir_path}/environments/{env_config_file_name}')
    result = default_config_json

    if client_config_file_name is not None:
        print(f'client config {client_config_file_name} specified...')
        client_config_json = import_local_json(f'{current_dir_path}/client/{client_config_file_name}')

        print(f'attempting to merge client config: {client_config_json} with default config: {env_config_file_name}')
        merged_config = merge_client_config(client_config_json, default_config_json)
        print(f'merge successful')
        result = merged_config

    return result


def create_container(solution_directory, env_config_file_name: str, client_config_file_name: str = None):
    current_dir_path = str.replace(solution_directory, '\\', '/')
    app_config_json = {
        "current_dir_path": current_dir_path
    }

    environment_config_json = import_and_merge_environment_configs(
        current_dir_path=current_dir_path,
        env_config_file_name=env_config_file_name,
        client_config_file_name=client_config_file_name
    )

    container = ApplicationContainer()
    container.config.app_config.from_dict(app_config_json)
    container.config.environment_config.from_dict(environment_config_json)
    container.wire(modules=[sys.modules[__name__]])
    return container


if __name__ == '__main__':
    main()
