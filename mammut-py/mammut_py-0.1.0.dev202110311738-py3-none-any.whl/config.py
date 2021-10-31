
from dynaconf import Dynaconf
import os

current_directory = os.path.dirname(os.path.realpath(__file__))

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=[f"{current_directory}/settings.toml", f"{current_directory}/.secrets.toml"],
)

HOME = os.path.expanduser("~")
save_folder = os.path.join(HOME, '.mammut-py', 'curriculum')

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load this files in the order.

