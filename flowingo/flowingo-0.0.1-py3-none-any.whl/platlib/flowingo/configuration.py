import pathlib
from dataclasses import dataclass
from typing import Optional, Union


@dataclass
class Config:
    # Webserver
    webserver_port: int = 8080
    webserver_debug: bool = False
    webserver_demonize: bool = False

    # Manager
    manager_debug: bool = False
    manager_demonize: bool = False
    manager_pipelines_refresh_period: int = 60  # seconds
    # Folders
    pipelines_folder: Union[str, pathlib.Path] = '../pipelines'
    tasks_folder: Optional[Union[str, pathlib.Path]] = '../tasks'


def validate_config(conf: Config):
    # Webserver
    assert 1024 <= conf.webserver_port < 49152, f'{conf.webserver_port} is not appropriate port'

    # Folders
    assert pathlib.Path(conf.pipelines_folder).exists(), f'{conf.pipelines_folder} does not exist'
    assert pathlib.Path(conf.tasks_folder).exists(), f'{conf.tasks_folder} does not exist'


def initialize_config() -> Config:
    """ Load the Flowingo config (from env and conf files).
    Called automatically as part of the boot process.
    """

    conf = Config()

    # Update from env
    pass

    # Update from config file
    pass

    return conf


conf = initialize_config()
# validate_config(conf)
